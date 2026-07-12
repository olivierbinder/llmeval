# %% IMPORTS -----
import argparse
import re
from pathlib import Path
from typing import Any, Literal

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel
from sqlalchemy import create_engine

from llmeval.utils.config import (
    DATABASE_URL,
    MISTRAL_API_KEY,
    MODEL_MAX_TOKENS,
    MODEL_NAME,
    MODEL_TEMPERATURE,
)

# %% CONSTANTS -----
SQL_AGENT_GUIDE_PATH = Path("database/sql_agent_guide.md")
DEFAULT_TOP_K = 10
MAX_SQL_AGENT_ITERATIONS = 8
MAX_SQL_AGENT_SECONDS = 30
READ_ONLY_SQL_RE = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)
STOPPED_OUTPUT = "Agent stopped due to iteration limit or time limit."


# %% RESULT SCHEMA -----
SqlToolErrorReason = Literal[
    "ambiguous",
    "missing_data",
    "sql_error",
    "timeout",
]


class SqlToolResult(BaseModel):
    success: bool
    answer: str | None = None
    error_reason: SqlToolErrorReason | None = None
    raw_output: str | None = None
    error_message: str | None = None

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


# %% PROMPT -----
def load_sql_agent_guide(path: Path = SQL_AGENT_GUIDE_PATH) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_sql_agent_prefix(guide: str) -> str:
    return f"""Tu es un agent SQL specialise NBA.

Reponds toujours en francais, de facon concise.
Reponds en texte simple, sans markdown.
Genere et execute des requetes SQL SQLite pour repondre aux questions.
Si la question necessite une interpretation metier non evidente, un seuil arbitraire ou une donnee absente du schema, ne force pas une requete SQL. Reponds simplement que la question ne peut pas etre traitee de facon fiable par SQL.
Ne demande jamais de precision a l'utilisateur.
Quand tu connais la reponse finale, ecris exactement `Final Answer: ...`.
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

    try:
        agent = create_nba_sql_agent(verbose=verbose)
        result = agent.invoke({"input": question})
    except TimeoutError as error:
        return SqlToolResult(
            success=False,
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
                error_reason="timeout",
                error_message=error_message,
            )
        return SqlToolResult(
            success=False,
            error_reason="sql_error",
            error_message=error_message,
        )

    output = str(result.get("output", "")).strip()
    return _classify_sql_output(output)


def answer_sql_question(question: str, verbose: bool = False) -> str:
    result = run_sql_question(question, verbose=verbose)
    if result.answer:
        return result.answer
    return f"SQL tool failed: {result.error_reason or 'unknown'}"


def _classify_sql_output(output: str) -> SqlToolResult:
    if not output:
        return SqlToolResult(
            success=False,
            error_reason="missing_data",
            raw_output=output,
            error_message="empty SQL agent output",
        )

    output_lower = output.lower()

    if STOPPED_OUTPUT.lower() in output_lower:
        return SqlToolResult(
            success=False,
            error_reason="timeout",
            raw_output=output,
            error_message=output,
        )

    if "error:" in output_lower or "only select queries are allowed" in output_lower:
        return SqlToolResult(
            success=False,
            error_reason="sql_error",
            raw_output=output,
            error_message=output,
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
            error_reason="ambiguous",
            raw_output=output,
            error_message=output,
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
            error_reason="missing_data",
            raw_output=output,
            error_message=output,
        )

    return SqlToolResult(success=True, answer=output, raw_output=output)


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
