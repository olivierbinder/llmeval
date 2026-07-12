# %% IMPORTS -----
from statistics import mean

import pandas as pd
from pydantic_evals.reporting import EvaluationReport

from llmeval.utils.config import APP_TITLE
from llmeval.utils.eval_schemas import (
    EvalCasesFile,
    RagAnswerVisible,
    RagEvalInput,
    RagEvalMetadata,
    RagExpectedOutput,
)
from llmeval.utils.report_csv import SCORE_COLUMNS

ReportOutput = RagExpectedOutput | RagAnswerVisible | str


# %% MARKDOWN REPORT -----
def build_markdown_summary(
    details: pd.DataFrame,
    eval_file: EvalCasesFile,
    report: EvaluationReport[RagEvalInput, ReportOutput, RagEvalMetadata],
    execution_seconds: float,
) -> str:
    evaluated = details[details["status"] == "evaluated"]
    evaluator_failure_count = sum(len(case.evaluator_failures) for case in report.cases)

    lines = [
        f"# Evaluation RAGAS {APP_TITLE}",
        "",
        f"- **Jeu de questions** : `{eval_file.metadata.dataset_name}`",
        f"- **Version** : `v{eval_file.metadata.version}`",
        f"- **Experience** : `{eval_file.metadata.experiment_name}`",
        f"- **Duree d'execution** : `{_format_duration(execution_seconds)}`",
        f"- **Cas evalues** : `{len(report.cases)}`",
        f"- **Task failures** : `{len(report.failures)}`",
        f"- **Evaluator failures** : `{evaluator_failure_count}`",
        "",
        "## Scores moyens",
        "",
        "| Metrique | Score moyen | Couverture |",
        "|---|---:|---:|",
    ]

    for score_name in SCORE_COLUMNS:
        score_values = [_optional_float(value) for value in evaluated[score_name]]
        present_values = [value for value in score_values if value is not None]
        lines.append(
            f"| `{score_name}` | {_format_score(_mean(present_values))} | "
            f"{len(present_values)}/{len(evaluated)} |"
        )

    lines.extend(
        [
            "",
            "## Scores par categorie",
            "",
            _category_summary(evaluated),
            "",
            "## Synthese des cas",
            "",
            "| Cas | Statut | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |",
            "|---|---|---|---:|---:|---:|---:|---|---:|---:|",
        ]
    )

    for row in details.to_dict(orient="records"):
        lines.append(
            f"| {_md_cell(row.get('id_question'))} | "
            f"{_md_cell(row.get('status'))} | "
            f"{_md_cell(row.get('category'))} | "
            f"{_format_score(_optional_float(row.get('faithfulness')))} | "
            f"{_format_score(_optional_float(row.get('answer_relevancy')))} | "
            f"{_format_score(_optional_float(row.get('context_precision')))} | "
            f"{_format_score(_optional_float(row.get('context_recall')))} | "
            f"{_md_cell(row.get('confidence'))} | "
            f"{_md_cell(row.get('retrieval_context_count'))} | "
            f"{_md_cell(row.get('evaluator_failure_count'))} |"
        )

    error_lines = _error_summary(details)
    if error_lines:
        lines.extend(["", "## Erreurs", "", *error_lines])

    return "\n".join(lines) + "\n"


# %% MARKDOWN HELPERS -----
def _category_summary(evaluated: pd.DataFrame) -> str:
    if evaluated.empty:
        return "_Aucun cas evalue._"

    lines = [
        "| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    grouped = evaluated.groupby("category", dropna=False)
    for category, group in grouped:
        lines.append(
            f"| {_md_cell(category)} | "
            f"{len(group)} | "
            f"{_format_score(_column_mean(group, 'faithfulness'))} | "
            f"{_format_score(_column_mean(group, 'answer_relevancy'))} | "
            f"{_format_score(_column_mean(group, 'context_precision'))} | "
            f"{_format_score(_column_mean(group, 'context_recall'))} |"
        )

    return "\n".join(lines)


def _error_summary(details: pd.DataFrame) -> list[str]:
    lines: list[str] = []

    for row in details.to_dict(orient="records"):
        task_error = _clean_text(row.get("task_error"))
        evaluator_failures = _clean_text(row.get("evaluator_failures"))

        if task_error:
            lines.append(
                f"- `{row.get('id_question')}` task failed: {_md_cell(task_error)}"
            )

        if evaluator_failures:
            lines.append(
                f"- `{row.get('id_question')}` evaluator failed: "
                f"{_md_cell(evaluator_failures)}"
            )

    return lines


def _column_mean(data: pd.DataFrame, column: str) -> float | None:
    values = [_optional_float(value) for value in data[column].tolist()]
    values = [value for value in values if value is not None]
    return _mean(values)


def _mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def _optional_float(value: object) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None

        return float(value)
    except (TypeError, ValueError):
        return None


def _format_score(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    minutes, remaining_seconds = divmod(total_seconds, 60)
    hours, remaining_minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {remaining_minutes}min {remaining_seconds}s"

    if minutes:
        return f"{minutes}min {remaining_seconds}s"

    return f"{remaining_seconds}s"


def _md_cell(value: object) -> str:
    text = _clean_text(value)
    return text.replace("\n", "<br>").replace("|", "\\|") if text else "n/a"


def _clean_text(value: object) -> str:
    if value is None:
        return ""

    text = str(value).strip()
    return "" if not text or text.lower() in {"nan", "none"} else text
