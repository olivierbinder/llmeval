# %% IMPORTS -----
from typing import Any

import pandas as pd
from pydantic_evals.reporting import EvaluationReport

from llmeval.utils.eval_schemas import (
    EvalCasesFile,
    RagAnswer,
    RagAnswerVisible,
    RagEvalInput,
    RagEvalMetadata,
    RagExpectedOutput,
)

SCORE_COLUMNS = (
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall",
)
ReportOutput = RagExpectedOutput | RagAnswerVisible | str


# %% CSV REPORT -----
def build_report_dataframe(
    eval_file: EvalCasesFile,
    report: EvaluationReport[RagEvalInput, ReportOutput, RagEvalMetadata],
) -> pd.DataFrame:
    dataset = eval_file.metadata
    case_order = {case.id: index for index, case in enumerate(eval_file.cases, start=1)}
    rows: list[dict[str, Any]] = []

    for case in report.cases:
        visible_output = (
            case.output if isinstance(case.output, RagAnswerVisible) else None
        )
        full_output = _full_answer(case.output)
        row = _base_row(
            dataset_name=dataset.dataset_name,
            dataset_version=dataset.version,
            experiment_name=dataset.experiment_name,
            case_name=case.name,
            inputs=case.inputs,
            metadata=case.metadata,
            expected_output=case.expected_output,
        )
        row.update(
            {
                "status": "evaluated",
                "answer": _output_answer(case.output),
                "model": full_output.model if full_output else None,
                "retrieval_strategy": full_output.retrieval_strategy
                if full_output
                else None,
                "sql_error_reason": full_output.sql_error_reason
                if full_output
                else None,
                "used_sources": _join(visible_output.used_sources)
                if visible_output
                else None,
                "retrieved_sources": _join(
                    [context.source for context in full_output.contexts],
                )
                if full_output
                else None,
                "retrieved_scores": _join(
                    [f"{context.score:.3f}" for context in full_output.contexts],
                )
                if full_output
                else None,
                "retrieved_context_count": case.metrics.get(
                    "retrieval_context_count",
                    len(full_output.contexts) if full_output else None,
                ),
                "retrieval_top_score": case.metrics.get("retrieval_top_score"),
                "confidence": visible_output.confidence if visible_output else None,
                "insufficient_context": visible_output.insufficient_context
                if visible_output
                else None,
                "task_duration": case.task_duration,
                "total_duration": case.total_duration,
                "evaluator_failure_count": len(case.evaluator_failures),
                "evaluator_failures": _format_evaluator_failures(
                    case.evaluator_failures,
                ),
                "task_error": None,
            }
        )
        row.update(_metric_values(case.metrics))
        row.update(_attribute_values(case.attributes, existing_keys=set(row)))

        for score_name in SCORE_COLUMNS:
            score = case.scores.get(score_name)
            row[score_name] = _score_value(score)
            row[f"{score_name}_reason"] = _score_reason(score)

        rows.append(row)

    for failure in report.failures:
        row = _base_row(
            dataset_name=dataset.dataset_name,
            dataset_version=dataset.version,
            experiment_name=dataset.experiment_name,
            case_name=failure.name,
            inputs=failure.inputs,
            metadata=failure.metadata,
            expected_output=failure.expected_output,
        )
        row.update(
            {
                "status": "task_failed",
                "answer": None,
                "model": None,
                "retrieval_strategy": None,
                "sql_error_reason": None,
                "used_sources": None,
                "retrieved_sources": None,
                "retrieved_scores": None,
                "retrieved_context_count": None,
                "retrieval_top_score": None,
                "confidence": None,
                "insufficient_context": None,
                "task_duration": None,
                "total_duration": None,
                "evaluator_failure_count": None,
                "evaluator_failures": None,
                "task_error": failure.error_message,
            }
        )
        row.update(_failure_metric_values())

        for score_name in SCORE_COLUMNS:
            row[score_name] = None
            row[f"{score_name}_reason"] = None

        rows.append(row)

    return _sort_report_dataframe(pd.DataFrame(rows), case_order)


# %% ROW HELPERS -----
def _base_row(
    dataset_name: str,
    dataset_version: int,
    experiment_name: str,
    case_name: str,
    inputs: RagEvalInput,
    metadata: RagEvalMetadata | None,
    expected_output: object,
) -> dict[str, Any]:
    expected = (
        expected_output if isinstance(expected_output, RagExpectedOutput) else None
    )

    return {
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "experiment_name": experiment_name,
        "id_question": inputs.id_question,
        "case_order": inputs.case_order,
        "case_name": case_name,
        "category": metadata.category if metadata else None,
        "source_type": metadata.source_type if metadata else None,
        "language": metadata.language if metadata else None,
        "question": inputs.question,
        "reference_answer": expected.answer if expected else expected_output,
        "expected_behavior": expected.expected_behavior if expected else None,
        "expected_sources": _join(expected.expected_sources) if expected else None,
        "evidence_notes": metadata.evidence_notes if metadata else None,
    }


def _full_answer(output: object) -> RagAnswer | None:
    if isinstance(output, RagAnswer):
        return output

    if isinstance(output, RagAnswerVisible):
        return output.full_answer

    return None


def _output_answer(output: object) -> str | None:
    if isinstance(output, RagAnswerVisible):
        return output.answer

    if isinstance(output, RagAnswer):
        return output.answer

    return str(output) if output is not None else None


def _score_value(score: object) -> float | None:
    if score is None:
        return None

    value = getattr(score, "value", None)
    return float(value) if value is not None else None


def _score_reason(score: object) -> str | None:
    if score is None:
        return None

    reason = getattr(score, "reason", None)
    return str(reason) if reason else None


def _format_evaluator_failures(failures: list[object]) -> str | None:
    if not failures:
        return None

    return " | ".join(
        f"{getattr(failure, 'name', 'unknown')}: "
        f"{getattr(failure, 'error_message', 'unknown error')}"
        for failure in failures
    )


def _join(values: list[object]) -> str:
    return "; ".join(str(value) for value in values)


def _metric_values(metrics: dict[str, int | float]) -> dict[str, int | float]:
    return dict(metrics)


def _attribute_values(
    attributes: dict[str, Any],
    existing_keys: set[str],
) -> dict[str, Any]:
    values: dict[str, Any] = {}

    for name, value in attributes.items():
        key = name if name not in existing_keys else f"attribute_{name}"
        values[key] = value

    return values


def _failure_metric_values() -> dict[str, None]:
    metric_names = [
        "retrieval_seconds",
        "retrieval_context_count",
        "retrieval_mean_score",
        "retrieval_total_chars",
        "retrieved_source_count",
        "generation_seconds",
        "generation_wait_seconds",
        "generation_api_seconds",
        "answer_input_tokens",
        "answer_output_tokens",
        "answer_total_tokens",
        "answer_request_count",
        "answer_chars",
        "task_seconds",
        "ragas_total_seconds",
        "ragas_wait_seconds",
        "ragas_api_seconds",
        "judge_request_count",
        "judge_input_tokens",
        "judge_output_tokens",
        "judge_total_tokens",
        "embedding_request_count",
    ]
    prefixes = ["faithfulness", "relevancy", "precision", "recall"]
    suffixes = [
        "seconds",
        "score",
        "wait_seconds",
        "api_seconds",
        "request_count",
        "embedding_request_count",
        "input_tokens",
        "output_tokens",
        "total_tokens",
    ]

    values = {name: None for name in metric_names}
    values.update({f"{prefix}_{suffix}": None for prefix in prefixes for suffix in suffixes})
    return values


def _sort_report_dataframe(
    details: pd.DataFrame,
    case_order: dict[str, int],
) -> pd.DataFrame:
    if details.empty:
        return details

    details = details.copy()
    details["case_order"] = details.apply(
        lambda row: _case_order_value(row, case_order),
        axis=1,
    )
    return details.sort_values(
        by=["case_order", "id_question"],
        kind="stable",
    ).reset_index(drop=True)


def _case_order_value(row: pd.Series, case_order: dict[str, int]) -> int:
    try:
        value = row.get("case_order")
        if value is not None and not pd.isna(value):
            return int(value)
    except (TypeError, ValueError):
        pass

    id_question = str(row.get("id_question") or "")
    return case_order.get(id_question, len(case_order) + 1)
