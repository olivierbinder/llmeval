# %% IMPORTS -----
from pathlib import Path

from pydantic_evals.reporting import EvaluationReport

from llmeval.utils.eval_schemas import (
    EvalCasesFile,
    RagAnswerVisible,
    RagEvalInput,
    RagEvalMetadata,
    RagExpectedOutput,
)
from llmeval.utils.report_csv import build_report_dataframe
from llmeval.utils.report_md import build_markdown_summary

REPORTS_DIR = Path("reports")
ReportOutput = RagExpectedOutput | RagAnswerVisible | str


# %% EVAL REPORT -----
def write_reports(
    eval_file: EvalCasesFile,
    report: EvaluationReport[RagEvalInput, ReportOutput, RagEvalMetadata],
    execution_seconds: float,
) -> tuple[Path, Path]:
    REPORTS_DIR.mkdir(exist_ok=True)

    dataset_version = eval_file.metadata.version
    details_csv = REPORTS_DIR / f"nba_rag_eval_results_v{dataset_version}.csv"
    report_md = REPORTS_DIR / f"nba_rag_eval_report_v{dataset_version}.md"

    details = build_report_dataframe(eval_file, report)
    details.to_csv(details_csv, index=False)

    report_md.write_text(
        build_markdown_summary(
            details=details,
            eval_file=eval_file,
            report=report,
            execution_seconds=execution_seconds,
        ),
        encoding="utf-8",
    )

    return details_csv, report_md
