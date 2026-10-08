"""Tests du routage SQL/FAISS partagé entre l'évaluation et l'application.

Aucun appel réseau : le vector store, l'agent RAG et l'outil SQL sont remplacés
par des doubles.
"""

# %% IMPORTS -----
from typing import Any

import pytest

from llmeval.utils import answer_service
from llmeval.utils.answer_service import AnswerService
from llmeval.utils.eval_schemas import (
    GenerationStats,
    RagAnswer,
    RetrievedContext,
)
from llmeval.utils.sql_tool import SqlQueryEvidence, SqlToolResult

QUANTITATIVE_QUESTION = "Qui a le meilleur pourcentage de reussite aux tirs ?"
QUALITATIVE_QUESTION = "Que disent les commentaires sur Julius Randle ?"


# %% DOUBLES -----
class FakeVectorStore:
    def __init__(self) -> None:
        self.search_calls: list[tuple[str, int]] = []

    def search(self, query_text: str, k: int = 5, min_score: float | None = None) -> list[dict[str, Any]]:
        self.search_calls.append((query_text, k))
        return [
            {
                "score": 87.5,
                "raw_score": 0.875,
                "text": "Extrait Reddit sur Randle.",
                "metadata": {"source": "Reddit 1.pdf"},
            }
        ]


class FakeRagAgent:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def answer(
        self,
        case_id: str,
        question: str,
        contexts: list[RetrievedContext],
    ) -> RagAnswer:
        self.questions.append(question)
        return RagAnswer(
            question=question,
            answer="Reponse FAISS.",
            contexts=contexts,
            model="fake-model",
            used_sources=[ctx.source for ctx in contexts],
            confidence="medium",
            generation=GenerationStats(seconds=1.0, answer_chars=14),
        )


def _sql_success_result() -> SqlToolResult:
    return SqlToolResult(
        success=True,
        answer="Le meilleur pourcentage est de 45 %.",
        sql_evidence=[
            SqlQueryEvidence(
                query="SELECT player_name FROM players ORDER BY fg_pct DESC LIMIT 1",
                result="[('Jokic',)]",
            )
        ],
        api_stats=GenerationStats(seconds=2.0, total_tokens=120, request_count=2),
    )


def _sql_failure_result() -> SqlToolResult:
    return SqlToolResult(
        success=False,
        error_reason="missing_sql_evidence",
        error_message="aucune requete SQL observee",
        api_stats=GenerationStats(seconds=0.5, total_tokens=30, request_count=1),
    )


# %% FIXTURES -----
@pytest.fixture
def service() -> AnswerService:
    return AnswerService(vector_store=FakeVectorStore(), rag_agent=FakeRagAgent())


# %% TESTS -----
def test_sql_success_path(monkeypatch: pytest.MonkeyPatch, service: AnswerService) -> None:
    monkeypatch.setattr(answer_service, "run_sql_question", lambda question: _sql_success_result())

    answer = service.answer(QUANTITATIVE_QUESTION)

    assert answer.retrieval_strategy == "sql"
    assert answer.answer == "Le meilleur pourcentage est de 45 %."
    assert answer.used_sources == ["regular NBA.xlsx (Feuille: Données NBA)"]
    assert answer.contexts[0].metadata["retrieval_type"] == "sql"
    assert answer.contexts[0].metadata["sql_evidence"][0]["query"].startswith("SELECT")
    assert service.vector_store.search_calls == []
    assert service.rag_agent.questions == []


def test_sql_failure_falls_back_to_faiss(
    monkeypatch: pytest.MonkeyPatch,
    service: AnswerService,
) -> None:
    monkeypatch.setattr(answer_service, "run_sql_question", lambda question: _sql_failure_result())

    answer = service.answer(QUANTITATIVE_QUESTION)

    assert answer.retrieval_strategy == "sql_fallback_faiss"
    assert answer.sql_error_reason == "missing_sql_evidence"
    assert answer.answer == "Reponse FAISS."
    assert len(service.vector_store.search_calls) == 1
    assert service.rag_agent.questions == [QUANTITATIVE_QUESTION]
    # Les statistiques de la tentative SQL sont ajoutées à celles du repli FAISS.
    assert answer.generation.total_tokens == 30
    assert answer.generation.request_count == 1
    assert answer.generation.seconds == pytest.approx(1.5, abs=0.5)


def test_qualitative_question_never_calls_sql(
    monkeypatch: pytest.MonkeyPatch,
    service: AnswerService,
) -> None:
    def fail(question: str) -> SqlToolResult:
        raise AssertionError("run_sql_question ne doit pas être appelé")

    monkeypatch.setattr(answer_service, "run_sql_question", fail)

    answer = service.answer(QUALITATIVE_QUESTION)

    assert answer.retrieval_strategy == "faiss"
    assert answer.sql_error_reason is None
    assert len(service.vector_store.search_calls) == 1
    assert answer.retrieval.context_count == 1
    assert answer.retrieval.top_score == 87.5


def test_empty_question_is_rejected(service: AnswerService) -> None:
    with pytest.raises(ValueError):
        service.answer("   ")


def test_sql_failure_without_fallback_refuses(
    monkeypatch: pytest.MonkeyPatch,
    service: AnswerService,
) -> None:
    service.sql_fallback_to_faiss = False
    monkeypatch.setattr(answer_service, "run_sql_question", lambda question: _sql_failure_result())

    answer = service.answer(QUANTITATIVE_QUESTION)

    assert answer.retrieval_strategy == "sql"
    assert answer.insufficient_context is True
    assert answer.confidence == "low"
    assert service.vector_store.search_calls == []
