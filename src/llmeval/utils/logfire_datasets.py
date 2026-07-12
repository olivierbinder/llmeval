# %% IMPORTS -----
from typing import Any

import logfire
from logfire.experimental.api_client import LogfireAPIClient
from pydantic_evals import Dataset

from llmeval.utils.config import LOGFIRE_API_KEY
from llmeval.utils.eval_schemas import (
    EvalCasesFile,
    RagEvalInput,
    RagEvalMetadata,
    RagExpectedOutput,
)

HostedRagDataset = Dataset[RagEvalInput, RagExpectedOutput, RagEvalMetadata]


# %% HOSTED DATASET -----
def push_and_fetch_hosted_dataset(
    dataset: HostedRagDataset,
    eval_file: EvalCasesFile,
) -> HostedRagDataset:
    if not LOGFIRE_API_KEY:
        raise ValueError(
            "LOGFIRE_API_KEY is required to push and evaluate a hosted dataset."
        )

    description = build_dataset_description(eval_file)

    with logfire.span(
        "sync_logfire_dataset dataset_name={dataset_name}",
        dataset_name=dataset.name,
        dataset_version=eval_file.metadata.version,
        case_count=len(dataset.cases),
    ):
        with LogfireAPIClient(api_key=LOGFIRE_API_KEY) as client:
            hosted_info = client.push_dataset(
                dataset,
                description=description,
            )
            hosted_dataset = client.get_dataset(
                _hosted_dataset_ref(hosted_info, dataset.name),
                input_type=RagEvalInput,
                output_type=RagExpectedOutput,
                metadata_type=RagEvalMetadata,
            )

    if not isinstance(hosted_dataset, Dataset):
        raise TypeError("Logfire returned an unexpected dataset payload.")

    return hosted_dataset


def build_dataset_description(eval_file: EvalCasesFile) -> str:
    metadata = eval_file.metadata
    source_scope = "\n".join(f"- {source}" for source in metadata.source_scope)
    notes = "\n".join(f"- {note}" for note in metadata.notes)

    return "\n".join(
        [
            metadata.purpose.strip(),
            "",
            f"Dataset version: v{metadata.version}",
            f"Experiment name: {metadata.experiment_name}",
            f"Language: {metadata.language}",
            f"Source language: {metadata.source_language or 'n/a'}",
            "",
            "Source scope:",
            source_scope or "- n/a",
            "",
            "Notes:",
            notes or "- n/a",
        ]
    )


def _hosted_dataset_ref(hosted_info: dict[str, Any], fallback_name: str) -> str:
    return str(
        hosted_info.get("id")
        or hosted_info.get("dataset_id")
        or hosted_info.get("name")
        or fallback_name
    )
