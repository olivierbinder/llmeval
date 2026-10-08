"""Application Streamlit — NBA Analyst AI (RAG hybride FAISS + SQL).

Lancement local depuis la racine du dépôt :

    uv run streamlit run app/streamlit_app.py
"""

# %% IMPORTS -----
import hmac
import logging
import os
import sys
from pathlib import Path

import streamlit as st

# %% BOOTSTRAP -----
REPO_ROOT = Path(__file__).resolve().parents[1]

# Les chemins de llmeval.utils.config sont relatifs : on se place à la racine du
# dépôt avant tout import du paquet (les constantes sont lues à l'import).
os.chdir(REPO_ROOT)
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

st.set_page_config(
    page_title="NBA Analyst AI",
    page_icon="🏀",
    layout="wide",
)

# %% SECRETS -----
SECRET_KEYS = (
    "MISTRAL_API_KEY",
    "LOGFIRE_API_KEY",
    "LOGFIRE_TOKEN",
    "APP_PASSWORD",
    "QUESTION_LIMIT",
)


def _load_secrets() -> dict[str, str]:
    """Lit .streamlit/secrets.toml ou les secrets Streamlit Cloud, sans échouer."""
    try:
        raw = dict(st.secrets)
    except Exception:  # StreamlitSecretNotFoundError, FileNotFoundError, ...
        return {}

    return {key: str(raw[key]) for key in SECRET_KEYS if key in raw}


for _key, _value in _load_secrets().items():
    os.environ.setdefault(_key, _value)

# %% LLMEVAL IMPORTS (après le pont de secrets) -----
from llmeval.utils.answer_service import AnswerService  # noqa: E402
from llmeval.utils.config import (  # noqa: E402
    APP_TITLE,
    CASES_PATH,
    DATABASE_FILE,
    DOCUMENT_CHUNKS_FILE,
    EMBEDDING_MODEL,
    FAISS_INDEX_FILE,
    MODEL_NAME,
    RETRIEVAL_STRATEGY,
    SEARCH_K,
)
from llmeval.utils.eval_schemas import RagAnswer, load_eval_cases  # noqa: E402
from llmeval.utils.rag_agent import RagAgent  # noqa: E402
from llmeval.utils.vector_store import VectorStoreManager  # noqa: E402

DEFAULT_QUESTION_LIMIT = 20
CONTEXT_CHAR_LIMIT = 800
REPORT_FILES = {
    "Rapport d'évaluation v1 (10 questions)": "reports/nba_rag_eval_report_v1.md",
    "Rapport d'évaluation v0 (10 questions)": "reports/nba_rag_eval_report_v0.md",
    "Synthèse des résultats": "docs/04_resultats.md",
    "Pipeline RAG": "docs/02_pipeline_rag.md",
}


# %% CACHED RESOURCES -----
@st.cache_resource(show_spinner=False)
def load_vector_store() -> VectorStoreManager:
    missing = [
        path
        for path in (FAISS_INDEX_FILE, DOCUMENT_CHUNKS_FILE, DATABASE_FILE)
        if not Path(path).exists()
    ]
    if missing:
        raise FileNotFoundError(
            "Artefacts manquants : "
            + ", ".join(missing)
            + ". Régénère-les avec `uv run python -m llmeval.scripts.indexer` "
            "et `uv run python -m llmeval.ingestion.load_excel_to_db`."
        )

    vector_store = VectorStoreManager()
    if vector_store.index is None or not vector_store.document_chunks:
        raise RuntimeError(
            "Index FAISS vide ou illisible : vérifie vector_db/faiss_index.idx "
            "et vector_db/document_chunks.pkl."
        )

    return vector_store


def build_answer_service(vector_store: VectorStoreManager) -> AnswerService:
    """Construit un agent neuf à chaque exécution du script Streamlit.

    Chaque rerun Streamlit s'exécute dans une nouvelle boucle asyncio. Mettre
    l'agent en cache réutiliserait le client HTTP (httpx) et ses connexions
    keep-alive liées à l'ancienne boucle, ce qui provoque un
    `RuntimeError: ... is bound to a different event loop` à la question
    suivante. Seul l'index FAISS (lecture disque) est mis en cache.
    """
    return AnswerService(
        vector_store=vector_store,
        rag_agent=RagAgent(),
        search_k=SEARCH_K,
    )


@st.cache_data(show_spinner=False)
def load_example_questions() -> list[tuple[str, str]]:
    try:
        eval_file = load_eval_cases(CASES_PATH)
    except Exception:
        return []

    return [(case.id, case.question) for case in eval_file.cases]


# %% AUTH & QUOTA -----
def _question_limit() -> int:
    try:
        return max(1, int(os.getenv("QUESTION_LIMIT", DEFAULT_QUESTION_LIMIT)))
    except ValueError:
        return DEFAULT_QUESTION_LIMIT


def _require_password() -> bool:
    expected = os.getenv("APP_PASSWORD")
    if not expected:
        return True

    if st.session_state.get("authenticated"):
        return True

    st.title(f"🏀 {APP_TITLE}")
    st.caption("Application protégée par mot de passe.")
    provided = st.text_input("Mot de passe", type="password")
    if provided and hmac.compare_digest(provided, expected):
        st.session_state["authenticated"] = True
        st.rerun()
    elif provided:
        st.error("Mot de passe incorrect.")

    return False


def _quota_left() -> int:
    return _question_limit() - int(st.session_state.get("asked", 0))


# %% RENDERING -----
def _render_badges(answer: RagAnswer) -> None:
    labels = {
        "faiss": "Recherche vectorielle",
        "sql": "Requête SQL",
        "sql_fallback_faiss": "SQL puis repli vectoriel",
    }
    confidence = {"low": "confiance faible", "medium": "confiance moyenne", "high": "confiance élevée"}
    parts = [
        f"**Stratégie** : {labels.get(answer.retrieval_strategy, answer.retrieval_strategy)}",
        f"**{confidence.get(answer.confidence, answer.confidence)}**",
        f"**Modèle** : `{answer.model}`",
    ]
    if answer.insufficient_context:
        parts.append("**Contexte insuffisant**")
    st.caption(" · ".join(parts))

    if answer.used_sources:
        st.markdown("Sources utilisées : " + " · ".join(f"`{source}`" for source in answer.used_sources))


def _render_metrics(answer: RagAnswer) -> None:
    retrieval = answer.retrieval
    generation = answer.generation
    columns = st.columns(4)
    columns[0].metric("Contextes", retrieval.context_count)
    columns[1].metric("Score max", f"{retrieval.top_score:.1f}" if retrieval.top_score else "—")
    columns[2].metric("Génération", f"{generation.seconds:.1f} s")
    columns[3].metric("Tokens", generation.total_tokens or "—")
    st.caption(
        f"Recherche {retrieval.seconds:.1f} s · attente {generation.wait_seconds:.1f} s · "
        f"API {generation.api_seconds:.1f} s · {generation.request_count} requête(s) LLM"
        + (f" · erreur SQL : `{answer.sql_error_reason}`" if answer.sql_error_reason else "")
    )


def _render_contexts(answer: RagAnswer) -> None:
    for index, context in enumerate(answer.contexts, start=1):
        evidence = context.metadata.get("sql_evidence")
        if evidence:
            for item in evidence:
                st.markdown(f"**Requête SQL {index}**")
                st.code(item.get("query", ""), language="sql")
                st.text(item.get("result", "")[:CONTEXT_CHAR_LIMIT])
            continue

        st.markdown(f"**{index}. `{context.source}`** — score {context.score:.1f}")
        st.text(context.text[:CONTEXT_CHAR_LIMIT])


def render_answer(answer: RagAnswer, show_contexts: bool, show_sql: bool) -> None:
    st.markdown(answer.answer)
    _render_badges(answer)

    has_sql = any(ctx.metadata.get("sql_evidence") for ctx in answer.contexts)
    with st.expander("Détails (métriques, contextes, SQL)", expanded=False):
        _render_metrics(answer)
        if show_contexts or (show_sql and has_sql):
            st.divider()
            st.markdown("**Contextes utilisés**")
            _render_contexts(answer)


def render_history(show_contexts: bool, show_sql: bool) -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            answer = message.get("answer")
            if answer is None:
                st.markdown(message["content"])
            else:
                render_answer(answer, show_contexts, show_sql)


# %% QUESTION HANDLING -----
def ask(question: str, service: AnswerService, show_contexts: bool, show_sql: bool) -> None:
    question = question.strip()
    if not question:
        return

    if _quota_left() <= 0:
        st.warning(
            f"Quota de {_question_limit()} questions atteint pour cette session. "
            "Recharge la page pour repartir d'une nouvelle session."
        )
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner(
                "Recherche de contextes puis génération de la réponse… "
                "(une question chiffrée peut prendre ~30 s)"
            ):
                answer = service.answer(question)
        except Exception as error:  # noqa: BLE001 - on affiche l'erreur à l'utilisateur
            logging.exception("Échec de la génération de la réponse")
            message = f"⚠️ Erreur : {error}"
            st.markdown(message)
            st.session_state.messages.append({"role": "assistant", "content": message})
            return

        st.session_state.asked = int(st.session_state.get("asked", 0)) + 1
        st.session_state.messages.append(
            {"role": "assistant", "content": answer.answer, "answer": answer}
        )
        render_answer(answer, show_contexts, show_sql)


# %% RESULTS PAGE -----
def render_results() -> None:
    st.header("Résultats & méthode")
    st.caption(
        "Rapports produits par `uv run evaluate` (pydantic-evals + RAGAS + Logfire), "
        "tels quels, sans recalcul côté application."
    )

    available = {
        label: REPO_ROOT / path
        for label, path in REPORT_FILES.items()
        if (REPO_ROOT / path).exists()
    }
    if not available:
        st.info("Aucun rapport versionné trouvé dans `reports/` ou `docs/`.")
        return

    label = st.selectbox("Document", list(available))
    path = available[label]
    st.caption(f"`{path.relative_to(REPO_ROOT)}`")
    st.divider()
    st.markdown(path.read_text(encoding="utf-8"))


# %% MAIN -----
@st.cache_resource(show_spinner=False)
def _configure_tracing(token: str) -> None:
    from llmeval.utils.observability import configure_logfire

    configure_logfire(token=token)


def main() -> None:
    if not _require_password():
        return

    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("asked", 0)

    logfire_token = os.getenv("LOGFIRE_API_KEY") or os.getenv("LOGFIRE_TOKEN")
    if logfire_token:
        _configure_tracing(logfire_token)

    if not os.getenv("MISTRAL_API_KEY"):
        st.error(
            "`MISTRAL_API_KEY` est absente. Ajoute-la dans `.streamlit/secrets.toml` "
            "en local ou dans les secrets de l'app Streamlit Cloud."
        )
        st.stop()

    try:
        vector_store = load_vector_store()
    except Exception as error:  # noqa: BLE001 - configuration à corriger
        st.error(f"Initialisation impossible : {error}")
        st.stop()

    # !! Sidebar -----
    with st.sidebar:
        st.title(f"🏀 {APP_TITLE}")
        st.caption(
            f"Modèle `{MODEL_NAME}` · embeddings `{EMBEDDING_MODEL}` · "
            f"k={SEARCH_K} · stratégie `{RETRIEVAL_STRATEGY}`"
        )
        st.metric("Questions restantes", _quota_left())
        st.caption(
            f"{vector_store.index.ntotal if vector_store.index else 0} "
            f"vecteurs · {len(vector_store.document_chunks)} chunks"
        )

        show_contexts = st.toggle("Afficher les contextes", value=False)
        show_sql = st.toggle("Afficher les requêtes SQL", value=True)

        if st.button("Réinitialiser la conversation"):
            st.session_state.messages = []
            st.rerun()

        view = st.radio("Vue", ["Assistant", "Résultats & méthode"], label_visibility="collapsed")

    if view == "Résultats & méthode":
        render_results()
        return

    st.header("Assistant NBA")
    st.caption(
        "Questions qualitatives (discussions Reddit indexées dans FAISS) et "
        "quantitatives (statistiques NBA en base SQLite)."
    )

    if not st.session_state.messages:
        examples = load_example_questions()
        if examples:
            with st.expander("Exemples de questions", expanded=True):
                for case_id, question in examples:
                    if st.button(f"{case_id} — {question}", key=f"example-{case_id}"):
                        st.session_state["pending"] = question

    render_history(show_contexts, show_sql)

    if _quota_left() <= 0:
        st.warning(f"Quota de {_question_limit()} questions atteint pour cette session.")
        return

    question = st.chat_input("Pose une question sur la NBA…") or st.session_state.pop(
        "pending", None
    )
    if question:
        ask(question, build_answer_service(vector_store), show_contexts, show_sql)


main()
