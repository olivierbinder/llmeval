# %% IMPORTS -----
import logging
import time
from typing import Any

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

from llmeval.utils.config import (
    CASES_PATH,
    REPORTS_DIR,
    SEARCH_K,
)
from llmeval.utils.eval_schemas import (
    EvalResult,
    RagasScores,
    RetrievedContext,
    load_eval_cases,
)
from llmeval.utils.observability import configure_logfire
from llmeval.utils.rag_agent import MistralRagasEmbeddings, MistralRagasLLM, RagAgent
from llmeval.utils.reports import write_reports
from llmeval.utils.vector_store import VectorStoreManager

RAGAS_METRICS = [
    ("faithfulness", faithfulness),
    ("answer_relevancy", answer_relevancy),
    ("context_precision", context_precision),
    ("context_recall", context_recall),
]

RAGAS_RUN_CONFIG = RunConfig(
    max_workers=1,
    timeout=180,
    max_retries=6,
    max_wait=30,
)


# %% EVALUATION PIPELINE -----
def main() -> None:
    started_at = time.perf_counter()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    configure_logfire()
    REPORTS_DIR.mkdir(exist_ok=True)

    with logfire.span("evaluate_ragas_pipeline"):
        # !! Load evaluation cases -----
        with logfire.span("load_eval_cases path={path}", path=str(CASES_PATH)):
            eval_file = load_eval_cases(CASES_PATH)

        dataset_name = eval_file.metadata.dataset_name
        dataset_version = eval_file.metadata.version
        experiment_name = eval_file.metadata.experiment_name

        logging.info(
            "Loaded %s evaluation cases from dataset %s v%s - experiment %s",
            len(eval_file.cases),
            dataset_name,
            dataset_version,
            experiment_name,
        )

        # !! Initialize RAG components -----
        with logfire.span("initialize_rag_components"):
            vector_store = VectorStoreManager()
            rag_agent = RagAgent()

        results: list[EvalResult] = []

        # !! Generate answers -----
        with logfire.span(
            "generate_answers case_count={case_count}",
            case_count=len(eval_file.cases),
        ):
            for case in eval_file.cases:
                with logfire.span(
                    "evaluate_case case_id={case_id}",
                    case_id=case.id,
                    category=case.category,
                    source_type=case.source_type,
                    question=case.question,
                ):
                    with logfire.span(
                        "search_contexts case_id={case_id}",
                        case_id=case.id,
                        search_k=SEARCH_K,
                    ):
                        search_results = vector_store.search(
                            case.question,
                            k=SEARCH_K,
                        )
                        contexts = [
                            RetrievedContext.from_search_result(item)
                            for item in search_results
                        ]

                    with logfire.span(
                        "generate_rag_answer case_id={case_id}",
                        case_id=case.id,
                        context_count=len(contexts),
                    ):
                        rag_answer = rag_agent.answer(
                            case.id,
                            case.question,
                            contexts,
                        )

                    results.append(EvalResult(case=case, rag_answer=rag_answer))

                    logging.info(
                        "Generated answer for %s with %s contexts",
                        case.id,
                        len(contexts),
                    )

        # !! Analyze answers -----
        with logfire.span(
            "run_ragas case_count={case_count}",
            case_count=len(results),
            metrics=[metric_name for metric_name, _ in RAGAS_METRICS],
        ):
            apply_ragas_scores(results)

        # !! Write reports -----
        execution_seconds = time.perf_counter() - started_at

        with logfire.span(
            "write_reports dataset_version={dataset_version}",
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            experiment_name=experiment_name,
            execution_seconds=execution_seconds,
        ):
            details_csv, report_md = write_reports(
                results=results,
                dataset_name=dataset_name,
                dataset_version=dataset_version,
                experiment_name=experiment_name,
                execution_seconds=execution_seconds,
            )

        logging.info("Wrote %s", details_csv)
        logging.info("Wrote %s", report_md)


# %% RAGAS EVALUATION WITH MISTRAL WRAPPERS -----
def apply_ragas_scores(results: list[EvalResult]) -> None:
    dataset = _build_ragas_dataset(results)

    llm = MistralRagasLLM()
    embeddings = MistralRagasEmbeddings()

    scores_by_case: list[dict[str, float | None]] = [
        {
            "faithfulness": None,
            "answer_relevancy": None,
            "context_precision": None,
            "context_recall": None,
        }
        for _ in results
    ]

    for metric_name, metric in RAGAS_METRICS:
        with logfire.span(
            "evaluate_ragas_metric metric_name={metric_name}",
            metric_name=metric_name,
            case_count=len(results),
        ):
            logging.info("Running RAGAS metric: %s", metric_name)

            metric_result = evaluate(
                dataset=dataset,
                metrics=[metric],
                llm=llm,
                embeddings=embeddings,
                raise_exceptions=True,
                show_progress=True,
                run_config=RAGAS_RUN_CONFIG,
            )

            metric_df = metric_result.to_pandas()
            missing_count = 0

            for index, row in enumerate(metric_df.to_dict(orient="records")):
                score = _extract_metric_score(row, metric_name)
                scores_by_case[index][metric_name] = score

                if score is None:
                    missing_count += 1

            logging.info(
                "Finished RAGAS metric %s with %s missing score(s)",
                metric_name,
                missing_count,
            )

    for index, result in enumerate(results):
        row = scores_by_case[index]

        result.scores = RagasScores(
            faithfulness=row["faithfulness"],
            answer_relevancy=row["answer_relevancy"],
            context_precision=row["context_precision"],
            context_recall=row["context_recall"],
        )


def _build_ragas_dataset(results: list[EvalResult]) -> Dataset:
    return Dataset.from_list(
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


def _extract_metric_score(
    row: dict[str, Any],
    metric_name: str,
) -> float | None:
    score = _optional_float(row.get(metric_name))

    if score is not None:
        return score

    logging.warning(
        "Missing RAGAS score for metric %s. Available columns: %s",
        metric_name,
        ", ".join(row.keys()),
    )

    return None


def _optional_float(value: object) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None

        return float(value)
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    main()
