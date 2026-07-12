# %% IMPORTS -----
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_validator,
)


# %% COMMON TYPES -----
ExpectedBehavior = Literal[
    "answer_from_context",
    "synthesize_multiple_contexts",
    "answer_from_noisy_question",
    "compute_from_structured_data",
    "refuse_or_qualify_missing_data",
]

Confidence = Literal["low", "medium", "high"]
RetrievalStrategy = Literal["faiss", "sql", "hybrid", "langchain"]


# %% YAML METADATA -----
class EvalMetadata(BaseModel):
    dataset_name: str
    version: int
    experiment_name: str = "default_experiment"
    language: str
    source_language: str | None = None
    purpose: str
    source_scope: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


# %% YAML CASES -----
class EvalCase(BaseModel):
    id: str
    category: str
    source_type: str
    language: str
    question: str
    reference_answer: str
    expected_behavior: ExpectedBehavior
    expected_sources: list[str]
    evidence_notes: str

    @field_validator(
        "id",
        "category",
        "source_type",
        "language",
        "question",
        "reference_answer",
        "evidence_notes",
    )
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text field must not be empty")
        return value

    @field_validator("expected_sources")
    @classmethod
    def sources_must_not_be_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("expected_sources must contain at least one source")
        return value


# %% YAML FILE -----
class EvalCasesFile(BaseModel):
    metadata: EvalMetadata
    cases: list[EvalCase]

    @field_validator("cases")
    @classmethod
    def cases_must_not_be_empty(cls, value: list[EvalCase]) -> list[EvalCase]:
        if not value:
            raise ValueError("at least one evaluation case is required")
        return value


def load_eval_cases(path: str | Path) -> EvalCasesFile:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return EvalCasesFile.model_validate(raw)


# %% PYDANTIC EVALS INPUTS AND METADATA -----
class RagEvalInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_question: str = Field(
        validation_alias=AliasChoices("id_question", "case_id"),
    )
    question: str

    @property
    def case_id(self) -> str:
        return self.id_question

    @field_validator("id_question", "question")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text field must not be empty")
        return value


class RagExpectedOutput(BaseModel):
    answer: str
    expected_sources: list[str]
    expected_behavior: ExpectedBehavior

    @classmethod
    def from_eval_case(cls, case: EvalCase) -> "RagExpectedOutput":
        return cls(
            answer=case.reference_answer,
            expected_sources=case.expected_sources,
            expected_behavior=case.expected_behavior,
        )

    @field_validator("answer")
    @classmethod
    def answer_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("answer must not be empty")
        return value

    @field_validator("expected_sources")
    @classmethod
    def sources_must_not_be_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("expected_sources must contain at least one source")
        return value


class RagEvalMetadata(BaseModel):
    category: str
    source_type: str
    language: str
    evidence_notes: str

    @field_validator("category", "source_type", "language", "evidence_notes")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text field must not be empty")
        return value


# %% RETRIEVED CONTEXT -----
class RetrievedContext(BaseModel):
    text: str
    score: float
    source: str
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_search_result(cls, result: dict[str, Any]) -> "RetrievedContext":
        metadata = result.get("metadata") or {}

        return cls(
            text=result.get("text", ""),
            score=float(result.get("score", 0.0)),
            source=str(metadata.get("source", "source inconnue")),
            metadata=metadata,
        )


# %% RAG OUTPUT -----
class RetrievalStats(BaseModel):
    seconds: float = 0.0
    context_count: int = 0
    top_score: float | None = None
    mean_score: float | None = None
    total_chars: int = 0
    source_count: int = 0


class GenerationStats(BaseModel):
    seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    request_count: int = 0
    answer_chars: int = 0


class RagAnswer(BaseModel):
    question: str
    answer: str
    contexts: list[RetrievedContext]
    model: str
    used_sources: list[str] = Field(default_factory=list)
    insufficient_context: bool = False
    confidence: Confidence = "medium"
    retrieval: RetrievalStats = Field(default_factory=RetrievalStats)
    generation: GenerationStats = Field(default_factory=GenerationStats)

    def to_visible(self) -> "RagAnswerVisible":
        return RagAnswerVisible.from_answer(self)


class RagAnswerVisible(BaseModel):
    answer: str
    used_sources: list[str] = Field(default_factory=list)
    insufficient_context: bool = False
    confidence: Confidence = "medium"

    _full_answer: RagAnswer | None = PrivateAttr(default=None)

    @classmethod
    def from_answer(cls, answer: RagAnswer) -> "RagAnswerVisible":
        visible = cls(
            answer=answer.answer,
            used_sources=answer.used_sources,
            insufficient_context=answer.insufficient_context,
            confidence=answer.confidence,
        )
        visible._full_answer = answer
        return visible

    @property
    def full_answer(self) -> RagAnswer | None:
        return self._full_answer
