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
            "| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |",
            "|---|---|---|---|---:|---:|---:|---:|---|---:|---:|",
        ]
    )

    for row in details.to_dict(orient="records"):
        lines.append(
            f"| {_md_cell(row.get('id_question'))} | "
            f"{_md_cell(row.get('status'))} | "
            f"{_md_cell(row.get('retrieval_strategy'))} | "
            f"{_md_cell(row.get('category'))} | "
            f"{_format_score(_optional_float(row.get('faithfulness')))} | "
            f"{_format_score(_optional_float(row.get('answer_relevancy')))} | "
            f"{_format_score(_optional_float(row.get('context_precision')))} | "
            f"{_format_score(_optional_float(row.get('context_recall')))} | "
            f"{_md_cell(row.get('confidence'))} | "
            f"{_md_cell(row.get('retrieval_context_count'))} | "
            f"{_md_cell(row.get('evaluator_failure_count'))} |"
        )

    lines.extend(["", "## Performance", "", _performance_summary(evaluated)])

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


def _performance_summary(evaluated: pd.DataFrame) -> str:
    if evaluated.empty:
        return "_Aucun cas evalue._"

    lines = [
        "| Etape | Temps total | Attente | API | Appels LLM | Tokens entree | Tokens sortie |",
        "|---|---:|---:|---:|---:|---:|---:|",
        _performance_row(
            label="Reponses agent",
            data=evaluated,
            seconds="generation_seconds",
            wait="generation_wait_seconds",
            api="generation_api_seconds",
            calls="answer_request_count",
            input_tokens="answer_input_tokens",
            output_tokens="answer_output_tokens",
        ),
        _performance_row(
            label="RAGAS total",
            data=evaluated,
            seconds="ragas_total_seconds",
            wait="ragas_wait_seconds",
            api="ragas_api_seconds",
            calls="judge_request_count",
            input_tokens="judge_input_tokens",
            output_tokens="judge_output_tokens",
        ),
        "",
        "| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    metric_rows = [
        ("Faithfulness", "faithfulness"),
        ("Answer relevancy", "relevancy"),
        ("Context precision", "precision"),
        ("Context recall", "recall"),
    ]
    for label, prefix in metric_rows:
        lines.append(
            _performance_row(
                label=label,
                data=evaluated,
                seconds=f"{prefix}_seconds",
                wait=f"{prefix}_wait_seconds",
                api=f"{prefix}_api_seconds",
                calls=f"{prefix}_request_count",
                embedding_calls=f"{prefix}_embedding_request_count",
                input_tokens=f"{prefix}_input_tokens",
                output_tokens=f"{prefix}_output_tokens",
                aggregate="mean",
            )
        )

    lines.extend(
        [
            "",
            "Nombre d'appels API",
            "",
            "| Cas | Reponse agent | Faithfulness | Relevancy | Precision | Recall |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in evaluated.to_dict(orient="records"):
        lines.append(
            f"| {_md_cell(row.get('id_question'))} | "
            f"{_format_number(_optional_float(row.get('answer_request_count')))} | "
            f"{_metric_case_call_count(row, 'faithfulness')} | "
            f"{_metric_case_call_count(row, 'relevancy')} | "
            f"{_metric_case_call_count(row, 'precision')} | "
            f"{_metric_case_call_count(row, 'recall')} |"
        )

    return "\n".join(lines)


def _performance_row(
    label: str,
    data: pd.DataFrame,
    seconds: str,
    calls: str,
    input_tokens: str,
    output_tokens: str,
    wait: str | None = None,
    api: str | None = None,
    embedding_calls: str | None = None,
    aggregate: str = "sum",
) -> str:
    value = _column_mean if aggregate == "mean" else _column_sum
    embedding_cell = (
        f"{_format_number(value(data, embedding_calls))} | "
        if embedding_calls
        else ""
    )
    return (
        f"| {_md_cell(label)} | "
        f"{_format_seconds(value(data, seconds))} | "
        f"{_format_seconds(value(data, wait))} | "
        f"{_format_seconds(value(data, api))} | "
        f"{_format_number(value(data, calls))} | "
        f"{embedding_cell}"
        f"{_format_number(value(data, input_tokens))} | "
        f"{_format_number(value(data, output_tokens))} |"
    )


def _column_sum(data: pd.DataFrame, column: str | None) -> float | None:
    if not column or column not in data:
        return None

    values = [_optional_float(value) for value in data[column].tolist()]
    values = [value for value in values if value is not None]
    return sum(values) if values else None


def _metric_case_call_count(row: dict[str, object], prefix: str) -> str:
    judge_calls = _optional_float(row.get(f"{prefix}_request_count"))
    embedding_calls = _optional_float(row.get(f"{prefix}_embedding_request_count")) or 0
    if judge_calls is None and not embedding_calls:
        return "n/a"

    return _format_number((judge_calls or 0) + embedding_calls)


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


def _column_mean(data: pd.DataFrame, column: str | None) -> float | None:
    if not column or column not in data:
        return None

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


def _format_seconds(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f}s"


def _format_int(value: float | None) -> str:
    return "n/a" if value is None else f"{int(round(value))}"


def _format_number(value: float | None) -> str:
    if value is None:
        return "n/a"

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.1f}"


def _md_cell(value: object) -> str:
    text = _clean_text(value)
    return text.replace("\n", "<br>").replace("|", "\\|") if text else "n/a"


def _clean_text(value: object) -> str:
    if value is None:
        return ""

    text = str(value).strip()
    return "" if not text or text.lower() in {"nan", "none"} else text
