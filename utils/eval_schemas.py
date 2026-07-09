from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator


class EvalMetadata(BaseModel):
    dataset_name: str
    version: int
    language: str
    source_language: str | None = None
    purpose: str
    source_scope: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class EvalCase(BaseModel):
    id: str
    category: str
    source_type: str
    language: str
    question: str
    reference_answer: str
    expected_behavior: str
    expected_sources: list[str]
    evidence_notes: str

    @field_validator("question", "reference_answer", "evidence_notes")
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


class EvalCasesFile(BaseModel):
    metadata: EvalMetadata
    cases: list[EvalCase]

    @field_validator("cases")
    @classmethod
    def cases_must_not_be_empty(cls, value: list[EvalCase]) -> list[EvalCase]:
        if not value:
            raise ValueError("at least one evaluation case is required")
        return value


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


class RagAnswer(BaseModel):
    question: str
    answer: str
    contexts: list[RetrievedContext]
    model: str


class RagasScores(BaseModel):
    faithfulness: float | None = None
    answer_relevancy: float | None = None
    context_precision: float | None = None
    context_recall: float | None = None


class EvalResult(BaseModel):
    case: EvalCase
    rag_answer: RagAnswer
    scores: RagasScores = Field(default_factory=RagasScores)

    def to_flat_dict(self) -> dict[str, Any]:
        contexts = self.rag_answer.contexts
        return {
            "case_id": self.case.id,
            "category": self.case.category,
            "source_type": self.case.source_type,
            "language": self.case.language,
            "question": self.case.question,
            "reference_answer": self.case.reference_answer,
            "answer": self.rag_answer.answer,
            "expected_sources": "; ".join(self.case.expected_sources),
            "retrieved_sources": "; ".join(ctx.source for ctx in contexts),
            "retrieved_scores": "; ".join(f"{ctx.score:.2f}" for ctx in contexts),
            "faithfulness": self.scores.faithfulness,
            "answer_relevancy": self.scores.answer_relevancy,
            "context_precision": self.scores.context_precision,
            "context_recall": self.scores.context_recall,
        }


def load_eval_cases(path: str | Path) -> EvalCasesFile:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return EvalCasesFile.model_validate(raw)
