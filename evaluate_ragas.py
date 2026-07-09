import logging
from pathlib import Path
from statistics import mean

import logfire
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)
from ragas.run_config import RunConfig

from utils.eval_schemas import (
    EvalResult,
    RagasScores,
    RetrievedContext,
    load_eval_cases,
)
from utils.observability import configure_logfire
from utils.rag_agent import MistralRagasEmbeddings, MistralRagasLLM, RagAgent
from utils.vector_store import VectorStoreManager

CASES_PATH = Path("eval_cases/nba_eval_cases.yaml")
REPORTS_DIR = Path("reports")
DETAILS_CSV = REPORTS_DIR / "ragas_results.csv"
SUMMARY_CSV = REPORTS_DIR / "ragas_summary_by_category.csv"
SUMMARY_MD = REPORTS_DIR / "ragas_summary.md"
SEARCH_K = 5


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    configure_logfire()
    REPORTS_DIR.mkdir(exist_ok=True)

    with logfire.span("load_eval_cases path={path}", path=str(CASES_PATH)):
        eval_file = load_eval_cases(CASES_PATH)

    logging.info("Loaded %s evaluation cases", len(eval_file.cases))

    vector_store = VectorStoreManager()
    rag_agent = RagAgent()
    results: list[EvalResult] = []

    for case in eval_file.cases:
        with logfire.span(
            "evaluate_case case_id={case_id}",
            case_id=case.id,
            category=case.category,
            question=case.question,
        ):
            search_results = vector_store.search(case.question, k=SEARCH_K)
            contexts = [
                RetrievedContext.from_search_result(item) for item in search_results
            ]
            rag_answer = rag_agent.answer(case.question, contexts)
            results.append(EvalResult(case=case, rag_answer=rag_answer))
            logging.info(
                "Generated answer for %s with %s contexts", case.id, len(contexts)
            )

    with logfire.span("run_ragas case_count={case_count}", case_count=len(results)):
        apply_ragas_scores(results)

    write_reports(results)
    logging.info("Wrote %s", DETAILS_CSV)
    logging.info("Wrote %s", SUMMARY_CSV)
    logging.info("Wrote %s", SUMMARY_MD)


def apply_ragas_scores(results: list[EvalResult]) -> None:
    dataset = Dataset.from_list(
        [
            {
                "user_input": result.case.question,
                "response": result.rag_answer.answer,
                "retrieved_contexts": [ctx.text for ctx in result.rag_answer.contexts],
                "reference": result.case.reference_answer,
            }
            for result in results
        ]
    )

    ragas_result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=MistralRagasLLM(),
        embeddings=MistralRagasEmbeddings(),
        raise_exceptions=False,
        show_progress=True,
        run_config=RunConfig(
            max_workers=1,
            timeout=90,
            max_retries=3,
            max_wait=8,
        ),
    )
    scores_df = ragas_result.to_pandas()

    for index, result in enumerate(results):
        row = scores_df.iloc[index].to_dict()
        result.scores = RagasScores(
            faithfulness=_optional_float(row.get("faithfulness")),
            answer_relevancy=_optional_float(row.get("answer_relevancy")),
            context_precision=_optional_float(row.get("context_precision")),
            context_recall=_optional_float(row.get("context_recall")),
        )


def write_reports(results: list[EvalResult]) -> None:
    details = pd.DataFrame([result.to_flat_dict() for result in results])
    details.to_csv(DETAILS_CSV, index=False)

    score_columns = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall",
    ]
    summary = (
        details.groupby("category", dropna=False)[score_columns]
        .mean(numeric_only=True)
        .reset_index()
    )
    summary["case_count"] = details.groupby("category", dropna=False).size().values
    summary.to_csv(SUMMARY_CSV, index=False)

    SUMMARY_MD.write_text(build_markdown_summary(details, summary), encoding="utf-8")


def build_markdown_summary(details: pd.DataFrame, summary: pd.DataFrame) -> str:
    overall_scores = {
        column: _mean_without_none(details[column].tolist())
        for column in [
            "faithfulness",
            "answer_relevancy",
            "context_precision",
            "context_recall",
        ]
    }

    lines = [
        "# Evaluation RAGAS - phase 1",
        "",
        "## Scores moyens",
        "",
        "| Metrique | Score moyen |",
        "|---|---:|",
    ]
    for metric, score in overall_scores.items():
        lines.append(f"| {metric} | {_format_score(score)} |")

    lines.extend(
        [
            "",
            "## Scores par categorie",
            "",
            _summary_to_markdown(summary),
            "",
            "## Cas evalues",
            "",
            "| Cas | Categorie | Sources attendues | Sources retrouvees |",
            "|---|---|---|---|",
        ]
    )

    for row in details.to_dict(orient="records"):
        lines.append(
            f"| {row['case_id']} | {row['category']} | "
            f"{row['expected_sources']} | {row['retrieved_sources']} |"
        )

    lines.extend(
        [
            "",
            "## Lecture rapide",
            "",
            "- Les cas qualitatifs testent la capacite du RAG texte a retrouver et synthetiser les PDF Reddit.",
            "- Les cas quantitatifs testent les limites de l'Excel indexe comme texte.",
            "- Le cas Q10 doit rester prudent, car les donnees actuelles ne contiennent pas de split sur les cinq derniers matchs.",
        ]
    )
    return "\n".join(lines) + "\n"


def _optional_float(value: object) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _mean_without_none(values: list[object]) -> float | None:
    numeric_values = [_optional_float(value) for value in values]
    numeric_values = [value for value in numeric_values if value is not None]
    return mean(numeric_values) if numeric_values else None


def _format_score(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _summary_to_markdown(summary: pd.DataFrame) -> str:
    columns = [
        "category",
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall",
        "case_count",
    ]
    lines = [
        "| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary[columns].to_dict(orient="records"):
        lines.append(
            f"| {row['category']} | "
            f"{_format_score(_optional_float(row['faithfulness']))} | "
            f"{_format_score(_optional_float(row['answer_relevancy']))} | "
            f"{_format_score(_optional_float(row['context_precision']))} | "
            f"{_format_score(_optional_float(row['context_recall']))} | "
            f"{int(row['case_count'])} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
