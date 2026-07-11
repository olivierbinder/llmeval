# %% IMPORTS -----
from pathlib import Path
from statistics import mean

import pandas as pd

from llmeval.utils.config import (
    APP_TITLE,
    REPORTS_DIR,
)
from llmeval.utils.eval_schemas import (
    EvalResult,
)


# %% EVAL REPORT -----
def write_reports(
    results: list[EvalResult],
    dataset_name: str,
    dataset_version: int,
    experiment_name: str,
    execution_seconds: float,
) -> tuple[Path, Path]:
    details_csv = REPORTS_DIR / f"nba_rag_eval_results_v{dataset_version}.csv"
    report_md = REPORTS_DIR / f"nba_rag_eval_report_v{dataset_version}.md"

    details = pd.DataFrame([result.to_flat_dict() for result in results])
    details.insert(0, "dataset_name", dataset_name)
    details.insert(1, "dataset_version", dataset_version)
    details.insert(2, "experiment_name", experiment_name)
    details.to_csv(details_csv, index=False)

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

    report_md.write_text(
        build_markdown_summary(
            details=details,
            summary=summary,
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            experiment_name=experiment_name,
            execution_seconds=execution_seconds,
        ),
        encoding="utf-8",
    )

    return details_csv, report_md


# %% MARKDOWN REPORT -----
def build_markdown_summary(
    details: pd.DataFrame,
    summary: pd.DataFrame,
    dataset_name: str,
    dataset_version: int,
    experiment_name: str,
    execution_seconds: float,
) -> str:
    score_columns = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall",
    ]

    overall_scores = {
        column: _mean_without_none(details[column].tolist()) for column in score_columns
    }

    missing_scores_count = sum(
        1
        for row in details.to_dict(orient="records")
        for column in score_columns
        if _optional_float(row.get(column)) is None
    )

    total_scores_count = len(details) * len(score_columns)

    lines = [
        f"# Evaluation RAGAS {APP_TITLE}",
        "",
        f"- **Jeu de questions** : `{dataset_name}`",
        f"- **Version** : `v{dataset_version}`",
        f"- **Experience** : `{experiment_name}`",
        f"- **Duree d'execution** : `{_format_duration(execution_seconds)}`",
        f"- **Cas evalues** : `{len(details)}`",
        f"- **Scores RAGAS calcules** : `{total_scores_count - missing_scores_count}/{total_scores_count}`",
        "",
        "## Scores moyens",
        "",
        "| Metrique | Score moyen |",
        "|---|---:|",
    ]

    for metric, score in overall_scores.items():
        lines.append(f"| `{metric}` | {_score_badge(score)} |")

    lines.extend(
        [
            "",
            "## Scores par categorie",
            "",
            _summary_to_markdown(summary),
            "",
            "## Synthese des cas",
            "",
            "| Cas | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contexte insuffisant |",
            "|---|---|---:|---:|---:|---:|---|---:|",
        ]
    )

    for row in details.to_dict(orient="records"):
        lines.append(
            f"| {row['case_id']} | "
            f"{_md_cell(row['category'])} | "
            f"{_score_badge(_optional_float(row.get('faithfulness')))} | "
            f"{_score_badge(_optional_float(row.get('answer_relevancy')))} | "
            f"{_score_badge(_optional_float(row.get('context_precision')))} | "
            f"{_score_badge(_optional_float(row.get('context_recall')))} | "
            f"{_md_cell(row.get('confidence', 'n/a'))} | "
            f"{_format_bool(row.get('insufficient_context'))} |"
        )

    lines.extend(
        [
            "",
            "## Detail par cas",
            "",
        ]
    )

    for row in details.to_dict(orient="records"):
        lines.extend(_case_detail_to_markdown(row))

    return "\n".join(lines) + "\n"


def _case_detail_to_markdown(row: dict[str, object]) -> list[str]:
    case_id = str(row.get("case_id", "unknown"))
    category = str(row.get("category", "unknown"))

    return [
        f"### {case_id} — {category}",
        "",
        "| Champ | Valeur |",
        "|---|---|",
        f"| Source type | {_md_cell(row.get('source_type', 'n/a'))} |",
        f"| Confiance LLM | {_md_cell(row.get('confidence', 'n/a'))} |",
        f"| Contexte insuffisant | {_format_bool(row.get('insufficient_context'))} |",
        f"| Faithfulness | {_score_badge(_optional_float(row.get('faithfulness')))} |",
        f"| Answer relevancy | {_score_badge(_optional_float(row.get('answer_relevancy')))} |",
        f"| Context precision | {_score_badge(_optional_float(row.get('context_precision')))} |",
        f"| Context recall | {_score_badge(_optional_float(row.get('context_recall')))} |",
        f"| Sources attendues | {_md_cell(row.get('expected_sources', 'n/a'))} |",
        f"| Sources utilisees par le LLM | {_md_cell(_format_sources_unique(row.get('used_sources')))} |",
        f"| Sources retrouvees par FAISS | {_md_cell(_format_sources_unique(row.get('retrieved_sources')))} |",
        f"| Scores retrieval | {_md_cell(row.get('retrieved_scores', 'n/a'))} |",
        "",
        "**Question**",
        "",
        _quote_text(row.get("question", "")),
        "",
        "**Reponse attendue YAML**",
        "",
        _quote_text(row.get("reference_answer", "")),
        "",
        "**Reponse du LLM**",
        "",
        _quote_text(row.get("answer", "")),
        "",
    ]


# %% HELPERS -----
def _optional_float(value: object) -> float | None:
    try:
        if value is None or pd.isna(value):
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


def _format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    minutes, remaining_seconds = divmod(total_seconds, 60)
    hours, remaining_minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {remaining_minutes}min {remaining_seconds}s"

    if minutes:
        return f"{minutes}min {remaining_seconds}s"

    return f"{remaining_seconds}s"


def _format_bool(value: object) -> str:
    if isinstance(value, bool):
        return "oui" if value else "non"

    text = str(value).strip().lower()

    if text in {"true", "1", "yes", "oui"}:
        return "oui"

    if text in {"false", "0", "no", "non"}:
        return "non"

    return "n/a"


def _format_sources_unique(value: object) -> str:
    if value is None:
        return "n/a"

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none"}:
        return "n/a"

    sources = [source.strip() for source in text.split(";") if source.strip()]
    unique_sources = list(dict.fromkeys(sources))

    return "; ".join(unique_sources) if unique_sources else "n/a"


def _score_badge(value: float | None) -> str:
    if value is None:
        return (
            '<span style="display:inline-block; min-width:52px; padding:2px 6px; '
            "border-radius:4px; background-color:#eeeeee; color:#555555; "
            'text-align:center;">n/a</span>'
        )

    clipped_value = max(0.0, min(1.0, value))
    background_color = _score_color(clipped_value)
    text_color = "#000000" if 0.35 <= clipped_value <= 0.85 else "#ffffff"

    return (
        f'<span style="display:inline-block; min-width:52px; padding:2px 6px; '
        f"border-radius:4px; background-color:{background_color}; "
        f'color:{text_color}; text-align:center;">{clipped_value:.3f}</span>'
    )


def _score_color(value: float) -> str:
    if value < 0.5:
        ratio = value / 0.5
        red = 248
        green = round(105 + ratio * (235 - 105))
        blue = round(107 + ratio * (132 - 107))
    else:
        ratio = (value - 0.5) / 0.5
        red = round(235 + ratio * (99 - 235))
        green = round(235 + ratio * (190 - 235))
        blue = round(132 + ratio * (123 - 132))

    return f"#{red:02x}{green:02x}{blue:02x}"


def _md_cell(value: object) -> str:
    if value is None:
        return "n/a"

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none"}:
        return "n/a"

    return text.replace("\n", "<br>").replace("|", "\\|")


def _quote_text(value: object) -> str:
    if value is None:
        return "> n/a"

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none"}:
        return "> n/a"

    lines = text.splitlines()

    return "\n".join(f"> {line}" if line.strip() else ">" for line in lines)


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
            f"| {_md_cell(row['category'])} | "
            f"{_score_badge(_optional_float(row['faithfulness']))} | "
            f"{_score_badge(_optional_float(row['answer_relevancy']))} | "
            f"{_score_badge(_optional_float(row['context_precision']))} | "
            f"{_score_badge(_optional_float(row['context_recall']))} | "
            f"{int(row['case_count'])} |"
        )

    return "\n".join(lines)
