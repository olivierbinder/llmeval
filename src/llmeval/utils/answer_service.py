# %% IMPORTS -----
import re
import time
import unicodedata
from dataclasses import dataclass

import logfire

from llmeval.utils.config import (
    MODEL_NAME,
    RETRIEVAL_STRATEGY,
    SEARCH_K,
    SQL_FALLBACK_TO_FAISS,
    SQL_ROUTE_KEYWORDS,
    SQL_ROUTE_METRICS,
)
from llmeval.utils.eval_schemas import (
    GenerationStats,
    RagAnswer,
    RetrievalStats,
    RetrievalStrategy,
    RetrievedContext,
)
from llmeval.utils.rag_agent import RagAgent
from llmeval.utils.sql_tool import SqlToolResult, run_sql_question
from llmeval.utils.vector_store import VectorStoreManager

# %% CONSTANTS -----
SQL_TABLE_SOURCES = {
    "players": "regular NBA.xlsx (Feuille: Données NBA)",
    "teams": "regular NBA.xlsx (Feuille: Equipe)",
    "features": "regular NBA.xlsx (Feuille: Dictionnaire des données)",
}
SQL_TABLES = tuple(SQL_TABLE_SOURCES)
SQL_FALLBACK_SOURCE = "database/nba.db"
SQL_INSUFFICIENT_ANSWER = (
    "Les donnees disponibles ne permettent pas de repondre precisement a cette question."
)


# %% ANSWER SERVICE -----
@dataclass
class AnswerService:
    """Parcourt unique de réponse RAG : SQL si routé, sinon repli FAISS.

    Partagé par l'application Streamlit et le pipeline d'évaluation afin que les
    deux répondent exactement de la même façon.
    """

    vector_store: VectorStoreManager
    rag_agent: RagAgent
    search_k: int = SEARCH_K
    retrieval_strategy: str = RETRIEVAL_STRATEGY
    sql_fallback_to_faiss: bool = SQL_FALLBACK_TO_FAISS

    def answer(self, question: str, case_id: str | None = None) -> RagAnswer:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")

        if self.retrieval_strategy != "hybrid":
            return answer_with_faiss(
                question=question,
                vector_store=self.vector_store,
                rag_agent=self.rag_agent,
                retrieval_strategy="faiss",
                search_k=self.search_k,
                case_id=case_id,
            )

        sql_result: SqlToolResult | None = None
        sql_seconds = 0.0

        if should_try_sql(question):
            sql_started = time.perf_counter()
            with logfire.span(
                "sql_tool_answer question={question}",
                question=question,
                case_id=case_id,
            ):
                sql_result = run_sql_question(question)
            sql_seconds = time.perf_counter() - sql_started

            if sql_result.success and sql_result.answer:
                contexts = sql_contexts(question=question, sql_result=sql_result)
                used_sources = sql_used_sources(sql_result) or [SQL_FALLBACK_SOURCE]
                return RagAnswer(
                    question=question,
                    answer=sql_result.answer,
                    contexts=contexts,
                    model=MODEL_NAME,
                    retrieval_strategy="sql",
                    used_sources=used_sources,
                    insufficient_context=False,
                    confidence="high",
                    retrieval=retrieval_stats(contexts, 0.0),
                    generation=sql_result.api_stats.model_copy(
                        update={
                            "seconds": sql_seconds,
                            "answer_chars": len(sql_result.answer),
                        },
                    ),
                )

            if not self.sql_fallback_to_faiss:
                error_reason = sql_result.error_reason if sql_result else "sql_error"
                error_message = (
                    sql_result.error_message
                    if sql_result
                    else "SQL tool did not return a result."
                )
                used_sources = (
                    sql_used_sources(sql_result) if sql_result else []
                ) or [SQL_FALLBACK_SOURCE]
                return RagAnswer(
                    question=question,
                    answer=SQL_INSUFFICIENT_ANSWER,
                    contexts=[],
                    model=MODEL_NAME,
                    retrieval_strategy="sql",
                    sql_error_reason=error_reason,
                    used_sources=used_sources,
                    insufficient_context=True,
                    confidence="low",
                    generation=sql_result.api_stats.model_copy(
                        update={
                            "seconds": sql_seconds,
                            "answer_chars": len(error_message or ""),
                        },
                    )
                    if sql_result
                    else GenerationStats(answer_chars=len(error_message or "")),
                )

        fallback_strategy: RetrievalStrategy = (
            "sql_fallback_faiss" if sql_result and not sql_result.success else "faiss"
        )
        full_answer = answer_with_faiss(
            question=question,
            vector_store=self.vector_store,
            rag_agent=self.rag_agent,
            retrieval_strategy=fallback_strategy,
            search_k=self.search_k,
            sql_error_reason=sql_result.error_reason if sql_result else None,
            case_id=case_id,
        )

        if sql_result and not sql_result.success:
            full_answer.generation = add_sql_attempt_stats(
                generation=full_answer.generation,
                sql_result=sql_result,
                sql_seconds=sql_seconds,
            )

        return full_answer


# %% RETRIEVAL -----
def answer_with_faiss(
    question: str,
    vector_store: VectorStoreManager,
    rag_agent: RagAgent,
    retrieval_strategy: RetrievalStrategy,
    search_k: int = SEARCH_K,
    sql_error_reason: str | None = None,
    case_id: str | None = None,
) -> RagAnswer:
    with logfire.span(
        "search_contexts question={question}",
        question=question,
        case_id=case_id,
        search_k=search_k,
        retrieval_strategy=retrieval_strategy,
        sql_error_reason=sql_error_reason,
    ):
        retrieval_started = time.perf_counter()
        search_results = vector_store.search(question, k=search_k)
        retrieval_seconds = time.perf_counter() - retrieval_started
        contexts = [
            RetrievedContext.from_search_result(item) for item in search_results
        ]
        stats = retrieval_stats(contexts, retrieval_seconds)

    full_answer = rag_agent.answer(
        case_id=case_id or "app",
        question=question,
        contexts=contexts,
    )
    full_answer.retrieval = stats
    full_answer.retrieval_strategy = retrieval_strategy
    full_answer.sql_error_reason = sql_error_reason
    return full_answer


def retrieval_stats(
    contexts: list[RetrievedContext],
    seconds: float,
) -> RetrievalStats:
    scores = [context.score for context in contexts]
    sources = list(dict.fromkeys(context.source for context in contexts))

    return RetrievalStats(
        seconds=seconds,
        context_count=len(contexts),
        top_score=max(scores) if scores else None,
        mean_score=sum(scores) / len(scores) if scores else None,
        total_chars=sum(len(context.text) for context in contexts),
        source_count=len(sources),
    )


# %% SQL EVIDENCE -----
def sql_contexts(
    question: str,
    sql_result: SqlToolResult,
) -> list[RetrievedContext]:
    if not sql_result.sql_evidence:
        return []

    sources = sql_used_sources(sql_result)
    return [
        RetrievedContext(
            text=sql_context_text(
                question=question,
                sql_result=sql_result,
                sources=sources,
            ),
            score=1.0,
            source=sql_context_source(sources),
            metadata={
                "retrieval_type": "sql",
                "sql_evidence": [
                    evidence.model_dump() for evidence in sql_result.sql_evidence
                ],
            },
        )
    ]


def sql_context_text(
    question: str,
    sql_result: SqlToolResult,
    sources: list[str],
) -> str:
    parts = [f"Question SQL traitee : {question}"]
    multiple_queries = len(sql_result.sql_evidence) > 1

    for index, evidence in enumerate(sql_result.sql_evidence, start=1):
        suffix = f" {index}" if multiple_queries else ""
        parts.extend(
            [
                f"Requete SQL executee{suffix} :",
                evidence.query,
                f"Resultat SQL{suffix} :",
                evidence.result,
            ]
        )

    if sources:
        parts.extend(["Sources :", "; ".join(sources)])

    return "\n".join(parts)


def sql_used_sources(sql_result: SqlToolResult) -> list[str]:
    tables: list[str] = []
    for evidence in sql_result.sql_evidence:
        for table in sql_tables_from_query(evidence.query):
            if table not in tables:
                tables.append(table)

    return [SQL_TABLE_SOURCES[table] for table in tables]


def sql_tables_from_query(query: str) -> list[str]:
    normalized = re.sub(r"[`\"[\]]", " ", query.lower())
    return [
        table
        for table in SQL_TABLES
        if re.search(rf"\b{re.escape(table)}\b", normalized)
    ]


def sql_context_source(sources: list[str]) -> str:
    if len(sources) == 1:
        return sources[0]

    if sources:
        return "; ".join(sources)

    return SQL_FALLBACK_SOURCE


def add_sql_attempt_stats(
    generation: GenerationStats,
    sql_result: SqlToolResult,
    sql_seconds: float,
) -> GenerationStats:
    sql_stats = sql_result.api_stats
    return generation.model_copy(
        update={
            "seconds": generation.seconds + sql_seconds,
            "wait_seconds": generation.wait_seconds + sql_stats.wait_seconds,
            "api_seconds": generation.api_seconds + sql_stats.api_seconds,
            "input_tokens": generation.input_tokens + sql_stats.input_tokens,
            "output_tokens": generation.output_tokens + sql_stats.output_tokens,
            "total_tokens": generation.total_tokens + sql_stats.total_tokens,
            "request_count": generation.request_count + sql_stats.request_count,
        },
    )


# %% SQL ROUTING -----
def should_try_sql(question: str) -> bool:
    normalized = normalize_for_route(question)
    keywords = [normalize_for_route(keyword).strip() for keyword in SQL_ROUTE_KEYWORDS]
    metrics = [normalize_for_route(metric).strip() for metric in SQL_ROUTE_METRICS]

    return any(route_term_matches(normalized, keyword) for keyword in keywords) or any(
        route_term_matches(normalized, metric) for metric in metrics
    )


def normalize_for_route(text: str) -> str:
    without_accents = "".join(
        char
        for char in unicodedata.normalize("NFKD", text.lower())
        if not unicodedata.combining(char)
    )
    return f" {without_accents} "


def route_term_matches(question: str, term: str) -> bool:
    if not term:
        return False

    if any(not char.isalnum() for char in term):
        return term in question

    return re.search(rf"\b{re.escape(term)}\b", question) is not None
