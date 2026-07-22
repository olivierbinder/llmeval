# %% IMPORTS -----
import argparse
import ast
import re
import time
from pathlib import Path
from typing import Any, Literal

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_core.callbacks import BaseCallbackHandler
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

from llmeval.utils.config import (
    DATABASE_URL,
    MISTRAL_API_KEY,
    MODEL_MAX_TOKENS,
    MODEL_NAME,
    MODEL_TEMPERATURE,
)
from llmeval.utils.eval_schemas import GenerationStats

# %% CONSTANTS -----
SQL_AGENT_GUIDE_PATH = Path("database/sql_agent_guide.md")
DEFAULT_TOP_K = 10
MAX_SQL_AGENT_ITERATIONS = 12
MAX_SQL_AGENT_SECONDS = 30
MAX_SQL_EVIDENCE_RETRIES = 1
READ_ONLY_SQL_RE = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)
STOPPED_OUTPUT = "Agent stopped due to iteration limit or time limit."
SQL_EVIDENCE_RETRY_INSTRUCTION = """Pour cette question, execute d'abord une requete SQL avec l'outil de requete SQL.
Ne donne pas de reponse finale avant d'avoir observe le resultat SQL."""
SQL_REFORMULATION_MAX_TOKENS = min(MODEL_MAX_TOKENS, 300)


# %% RESULT SCHEMA -----
SqlToolErrorReason = Literal[
    "ambiguous",
    "missing_data",
    "missing_sql_evidence",
    "sql_error",
    "timeout",
]


class SqlQueryEvidence(BaseModel):
    query: str
    result: str


class SqlToolResult(BaseModel):
    success: bool
    answer: str | None = None
    sql_evidence: list[SqlQueryEvidence] = Field(default_factory=list)
    api_stats: GenerationStats = Field(default_factory=GenerationStats)
    error_reason: SqlToolErrorReason | None = None
    raw_output: str | None = None
    error_message: str | None = None
    observed_tools: list[str] = Field(default_factory=list)

    @property
    def fallback_to_rag(self) -> bool:
        return not self.success


# %% SAFE DATABASE -----
class ReadOnlySQLDatabase(SQLDatabase):
    def run(
        self,
        command: str,
        fetch: Literal["all", "one", "cursor"] = "all",
        include_columns: bool = False,
        *,
        parameters: dict[str, Any] | None = None,
        execution_options: dict[str, Any] | None = None,
    ) -> str | list[dict[str, Any]] | Any:
        if not READ_ONLY_SQL_RE.match(str(command)):
            raise ValueError("Only SELECT queries are allowed.")

        return super().run(
            command,
            fetch=fetch,
            include_columns=include_columns,
            parameters=parameters,
            execution_options=execution_options,
        )

    def run_no_throw(
        self,
        command: str,
        fetch: Literal["all", "one"] = "all",
        include_columns: bool = False,
        *,
        parameters: dict[str, Any] | None = None,
        execution_options: dict[str, Any] | None = None,
    ) -> str | list[dict[str, Any]] | Any:
        try:
            return self.run(
                command,
                fetch=fetch,
                include_columns=include_columns,
                parameters=parameters,
                execution_options=execution_options,
            )
        except Exception as error:
            return f"Error: {error}"


# %% LANGCHAIN API STATS -----
class MistralLangChainStatsCallback(BaseCallbackHandler):
    def __init__(self) -> None:
        self.stats = GenerationStats()
        self._started_at: dict[object, float] = {}

    def stats_snapshot(self) -> GenerationStats:
        return self.stats.model_copy()

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        **kwargs: Any,
    ) -> None:
        self._start(kwargs.get("run_id"))

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[object]],
        **kwargs: Any,
    ) -> None:
        self._start(kwargs.get("run_id"))

    def on_llm_end(self, response: object, **kwargs: Any) -> None:
        run_id = kwargs.get("run_id")
        started_at = self._started_at.pop(run_id, None)
        if started_at is not None:
            api_seconds = time.perf_counter() - started_at
            self.stats.api_seconds += api_seconds
            self.stats.seconds += api_seconds

        self.stats.request_count += 1
        input_tokens, output_tokens, total_tokens = _langchain_usage_tokens(response)
        self.stats.input_tokens += input_tokens
        self.stats.output_tokens += output_tokens
        self.stats.total_tokens += total_tokens

    def _start(self, run_id: object) -> None:
        if run_id is not None:
            self._started_at[run_id] = time.perf_counter()


# %% PROMPT -----
def load_sql_agent_guide(path: Path = SQL_AGENT_GUIDE_PATH) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_sql_agent_prefix(guide: str) -> str:
    return f"""Tu es un agent SQL specialise NBA.

Réponds toujours en français, en texte simple, sans markdown.
Réponds de façon concise, avec une phrase complète contenant un verbe.
Inclue les valeurs numériques utiles et reprends explicitement la métrique demandée.
Évite les réponses télégraphiques du type `Nom (valeur)`.

Pour répondre à une question chiffrée traitable avec le schéma, exécute toujours au moins une requête SQL avant la réponse finale.
Ne réponds jamais à partir de ta mémoire ou d'une estimation.
Dès qu'une requête SQL retourne une ligne suffisante pour répondre, arrête les appels outils et écris immédiatement `Final Answer: ...`.
Ne répète jamais la même requête SQL.

Si la question demande une donnée absente du schéma, une fenêtre non disponible, un split absent ou une interprétation métier arbitraire, n'exécute pas de requête forcée.
Réponds alors clairement que les données disponibles ne permettent pas de répondre fiablement.

Ne demande jamais de précision à l'utilisateur.
Quand tu connais la réponse finale, écris exactement `Final Answer: ...`.

Tu dois respecter strictement ce guide :


{guide}

Dialecte SQL : {{dialect}}
Nombre maximum de lignes a retourner par defaut : {{top_k}}
"""


# %% AGENT FACTORY -----
def create_nba_sql_database() -> ReadOnlySQLDatabase:
    engine = create_engine(DATABASE_URL, future=True)
    return ReadOnlySQLDatabase(
        engine=engine,
        include_tables=["players", "teams", "features"],
        sample_rows_in_table_info=2,
    )


def create_nba_sql_agent(verbose: bool = False):
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is required to use the SQL tool.")

    llm = ChatMistralAI(
        model_name=MODEL_NAME,
        api_key=MISTRAL_API_KEY,
        temperature=MODEL_TEMPERATURE,
        max_tokens=MODEL_MAX_TOKENS,
    )
    db = create_nba_sql_database()
    guide = load_sql_agent_guide()

    return create_sql_agent(
        llm=llm,
        db=db,
        prefix=build_sql_agent_prefix(guide),
        top_k=DEFAULT_TOP_K,
        max_iterations=MAX_SQL_AGENT_ITERATIONS,
        max_execution_time=MAX_SQL_AGENT_SECONDS,
        verbose=verbose,
        agent_executor_kwargs={
            "handle_parsing_errors": (
                "Format invalide. Si tu connais la reponse finale, ecris "
                "`Final Answer: ...`. Sinon utilise Action puis Action Input."
            ),
            "return_intermediate_steps": True,
        },
    )


# %% PUBLIC TOOL -----
def run_sql_question(question: str, verbose: bool = False) -> SqlToolResult:
    question = question.strip()
    if not question:
        raise ValueError("question must not be empty")

    stats_callback = MistralLangChainStatsCallback()
    try:
        agent = create_nba_sql_agent(verbose=verbose)
        for attempt in range(MAX_SQL_EVIDENCE_RETRIES + 1):
            result = agent.invoke(
                {"input": _sql_agent_input(question, attempt)},
                config={"callbacks": [stats_callback]},
            )
            classified = _classify_agent_result(result)
            if classified.success and classified.sql_evidence:
                return _with_reformulated_sql_answer(
                    question,
                    classified,
                    stats_callback,
                )

            if classified.error_reason != "missing_sql_evidence":
                return _with_api_stats(classified, stats_callback)

        return _with_api_stats(classified, stats_callback)
    except TimeoutError as error:
        return SqlToolResult(
            success=False,
            api_stats=stats_callback.stats_snapshot(),
            error_reason="timeout",
            error_message=str(error),
        )
    except Exception as error:
        error_message = str(error)
        if (
            "unsupported early_stopping_method" in error_message
            or "iteration limit" in error_message.lower()
            or "time limit" in error_message.lower()
        ):
            return SqlToolResult(
                success=False,
                api_stats=stats_callback.stats_snapshot(),
                error_reason="timeout",
                error_message=error_message,
            )
        return SqlToolResult(
            success=False,
            api_stats=stats_callback.stats_snapshot(),
            error_reason="sql_error",
            error_message=error_message,
        )


def _sql_agent_input(question: str, attempt: int) -> str:
    if attempt == 0:
        return question

    return f"{SQL_EVIDENCE_RETRY_INSTRUCTION}\n\nQuestion : {question}"


def _with_reformulated_sql_answer(
    question: str,
    result: SqlToolResult,
    stats_callback: MistralLangChainStatsCallback,
) -> SqlToolResult:
    try:
        answer = _reformulate_sql_answer(
            question,
            result.sql_evidence,
            stats_callback,
        )
    except Exception:
        answer = result.answer or _fallback_answer_from_sql_evidence(
            result.sql_evidence
        )

    return _with_api_stats(
        result.model_copy(update={"answer": answer}),
        stats_callback,
    )


def _with_api_stats(
    result: SqlToolResult,
    stats_callback: MistralLangChainStatsCallback,
) -> SqlToolResult:
    stats = stats_callback.stats_snapshot()
    stats.answer_chars = len(result.answer or "")
    return result.model_copy(update={"api_stats": stats})


def _reformulate_sql_answer(
    question: str,
    sql_evidence: list[SqlQueryEvidence],
    stats_callback: MistralLangChainStatsCallback,
) -> str:
    if not sql_evidence:
        raise ValueError("sql_evidence must not be empty")

    evidence = sql_evidence[-1]
    llm = ChatMistralAI(
        model_name=MODEL_NAME,
        api_key=MISTRAL_API_KEY,
        temperature=0,
        max_tokens=SQL_REFORMULATION_MAX_TOKENS,
    )
    response = llm.invoke(
        _build_sql_reformulation_prompt(question, evidence),
        config={"callbacks": [stats_callback]},
    )
    answer = _message_content(response).strip()
    answer = re.sub(r"^Final Answer:\s*", "", answer, flags=re.IGNORECASE).strip()
    if not answer:
        raise ValueError("empty SQL reformulation")

    return answer


def _build_sql_reformulation_prompt(
    question: str,
    evidence: SqlQueryEvidence,
) -> str:
    return f"""Tu reformules un resultat SQL NBA en reponse finale.

Question utilisateur :
{question}

Requete SQL executee :
{evidence.query}

Resultat SQL observe :
{evidence.result}

Contraintes :
- Reponds en francais, en texte simple, sans markdown.
- Ecris une seule phrase concise, complete, avec un verbe.
- Base-toi uniquement sur le resultat SQL observe.
- Inclue les valeurs numeriques utiles et la metrique demandee.
- Si le resultat SQL est vide, dis que les donnees disponibles ne permettent pas de repondre.

Reponse finale :"""


def _message_content(response: object) -> str:
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("content") or ""))
            else:
                parts.append(str(item))
        return " ".join(part for part in parts if part)

    return str(content)


def _langchain_usage_tokens(response: object) -> tuple[int, int, int]:
    for usage in _langchain_usage_candidates(response):
        input_tokens, output_tokens, total_tokens = _usage_triplet(usage)
        if input_tokens or output_tokens or total_tokens:
            return input_tokens, output_tokens, total_tokens

    return 0, 0, 0


def _langchain_usage_candidates(response: object) -> list[object]:
    candidates: list[object] = []
    llm_output = getattr(response, "llm_output", None)
    candidates.extend(_usage_candidates_from_mapping(llm_output))

    generations = getattr(response, "generations", [])
    for generation_list in generations or []:
        for generation in generation_list or []:
            message = getattr(generation, "message", None)
            candidates.extend(
                [
                    getattr(message, "usage_metadata", None),
                    getattr(message, "response_metadata", None),
                    getattr(generation, "generation_info", None),
                ]
            )

    nested_candidates: list[object] = []
    for candidate in candidates:
        nested_candidates.append(candidate)
        nested_candidates.extend(_usage_candidates_from_mapping(candidate))

    return nested_candidates


def _usage_candidates_from_mapping(value: object) -> list[object]:
    if not isinstance(value, dict):
        return []

    return [
        value.get("token_usage"),
        value.get("usage"),
        value.get("usage_metadata"),
    ]


def _usage_triplet(usage: object) -> tuple[int, int, int]:
    input_tokens = _first_int_value(
        usage,
        ("input_tokens", "prompt_tokens", "prompt_token_count"),
    )
    output_tokens = _first_int_value(
        usage,
        ("output_tokens", "completion_tokens", "completion_token_count"),
    )
    total_tokens = _first_int_value(
        usage,
        ("total_tokens", "total_token_count"),
    )
    if not total_tokens:
        total_tokens = input_tokens + output_tokens

    return input_tokens, output_tokens, total_tokens


def _first_int_value(value: object, names: tuple[str, ...]) -> int:
    for name in names:
        int_value = _int_value(value, name)
        if int_value:
            return int_value

    return 0


def _int_value(value: object, name: str) -> int:
    raw_value = value.get(name) if isinstance(value, dict) else getattr(value, name, 0)
    return int(raw_value or 0)


def _classify_agent_result(result: dict[str, Any]) -> SqlToolResult:
    output = str(result.get("output", "")).strip()
    intermediate_steps = result.get("intermediate_steps", [])
    sql_evidence = _extract_sql_evidence(intermediate_steps)
    observed_tools = _extract_observed_tools(intermediate_steps)
    return _classify_sql_output(
        output,
        sql_evidence=sql_evidence,
        observed_tools=observed_tools,
    )


def answer_sql_question(question: str, verbose: bool = False) -> str:
    result = run_sql_question(question, verbose=verbose)
    if result.answer:
        return result.answer
    return f"SQL tool failed: {result.error_reason or 'unknown'}"


def _classify_sql_output(
    output: str,
    sql_evidence: list[SqlQueryEvidence] | None = None,
    observed_tools: list[str] | None = None,
) -> SqlToolResult:
    sql_evidence = sql_evidence or []
    observed_tools = observed_tools or []

    if not output:
        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="missing_data",
            raw_output=output,
            error_message="empty SQL agent output",
            observed_tools=observed_tools,
        )

    output_lower = output.lower()

    if STOPPED_OUTPUT.lower() in output_lower:
        if sql_evidence:
            return SqlToolResult(
                success=True,
                answer=_fallback_answer_from_sql_evidence(sql_evidence),
                sql_evidence=sql_evidence,
                raw_output=output,
                observed_tools=observed_tools,
            )

        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="timeout",
            raw_output=output,
            error_message=output,
            observed_tools=observed_tools,
        )

    if "error:" in output_lower or "only select queries are allowed" in output_lower:
        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="sql_error",
            raw_output=output,
            error_message=output,
            observed_tools=observed_tools,
        )

    ambiguous_markers = [
        "ambigu",
        "pas etre traitee de facon fiable par sql",
        "ne peut pas etre traitee de facon fiable par sql",
        "ne peut pas être traitée de façon fiable par sql",
        "seuil arbitraire",
        "doit etre precisee",
        "doit être précisée",
    ]
    if any(marker in output_lower for marker in ambiguous_markers):
        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="ambiguous",
            raw_output=output,
            error_message=output,
            observed_tools=observed_tools,
        )

    missing_data_markers = [
        "aucune donnee",
        "aucune donnée",
        "donnee absente",
        "donnée absente",
        "n'est pas disponible",
        "ne fournit pas",
        "pas de donnees",
        "pas de données",
    ]
    if any(marker in output_lower for marker in missing_data_markers):
        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="missing_data",
            raw_output=output,
            error_message=output,
            observed_tools=observed_tools,
        )

    if not sql_evidence:
        tools = ", ".join(observed_tools) if observed_tools else "none"
        return SqlToolResult(
            success=False,
            sql_evidence=sql_evidence,
            error_reason="missing_sql_evidence",
            raw_output=output,
            error_message=(
                "SQL agent returned an answer without captured sql_db_query "
                f"evidence. Observed tools: {tools}."
            ),
            observed_tools=observed_tools,
        )

    return SqlToolResult(
        success=True,
        answer=output,
        sql_evidence=sql_evidence,
        raw_output=output,
        observed_tools=observed_tools,
    )


def _fallback_answer_from_sql_evidence(sql_evidence: list[SqlQueryEvidence]) -> str:
    result = sql_evidence[-1].result.strip()
    return f"Le resultat SQL retourne : {_format_sql_result(result)}"


def _format_sql_result(result: str) -> str:
    try:
        parsed = ast.literal_eval(result)
    except (SyntaxError, ValueError):
        return result

    if not isinstance(parsed, list):
        return result

    rows = [_format_sql_row(row) for row in parsed]
    return "; ".join(row for row in rows if row) or result


def _format_sql_row(row: object) -> str:
    if isinstance(row, tuple | list):
        return ", ".join(str(value) for value in row)

    return str(row)


def _extract_sql_evidence(intermediate_steps: object) -> list[SqlQueryEvidence]:
    evidence: list[SqlQueryEvidence] = []
    for step in _iter_intermediate_steps(intermediate_steps):
        action, observation = step
        tool_name = str(getattr(action, "tool", "")).lower()
        query = _stringify_tool_input(getattr(action, "tool_input", "")).strip()
        if not _is_sql_query_tool_call(tool_name, query):
            continue

        result = str(observation).strip()
        if query:
            evidence.append(SqlQueryEvidence(query=query, result=result))

    return evidence


def _extract_observed_tools(intermediate_steps: object) -> list[str]:
    tools: list[str] = []
    for action, _observation in _iter_intermediate_steps(intermediate_steps):
        tool = str(getattr(action, "tool", "")).strip()
        if tool and tool not in tools:
            tools.append(tool)

    return tools


def _is_sql_query_tool_call(tool_name: str, query: str) -> bool:
    if tool_name == "sql_db_query":
        return True

    if "checker" in tool_name:
        return False

    return "query" in tool_name and READ_ONLY_SQL_RE.match(query) is not None


def _iter_intermediate_steps(intermediate_steps: object) -> list[tuple[object, object]]:
    if not isinstance(intermediate_steps, list):
        return []

    steps: list[tuple[object, object]] = []
    for step in intermediate_steps:
        if isinstance(step, tuple) and len(step) == 2:
            steps.append(step)

    return steps


def _stringify_tool_input(tool_input: object) -> str:
    if isinstance(tool_input, dict):
        return " ".join(str(value) for value in tool_input.values())

    return str(tool_input)


# %% CLI -----
def main() -> None:
    parser = argparse.ArgumentParser(description="Pose une question SQL sur nba.db")
    parser.add_argument("question", type=str)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_sql_question(args.question, verbose=args.verbose)
    if args.json:
        print(result.model_dump_json(indent=2))
    else:
        print(result.answer or result.error_message or result.error_reason)


if __name__ == "__main__":
    main()
