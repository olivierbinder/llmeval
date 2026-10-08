# %% IMPORTS -----
import os
from pathlib import Path

from dotenv import load_dotenv

# %% ENVIRONMENT VARIABLES -----
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    print(
        "⚠️ Attention: La clé API Mistral (MISTRAL_API_KEY) "
        "n'est pas définie dans le fichier .env"
    )
LOGFIRE_API_KEY = os.getenv("LOGFIRE_API_KEY")
if not LOGFIRE_API_KEY:
    print(
        "⚠️ Attention: La clé API Logfire (LOGFIRE_API_KEY) "
        "n'est pas définie dans le fichier .env"
    )

# %% MISTRAL MODELS -----
MISTRAL_API_BASE_URL = "https://api.mistral.ai/v1"
# Surchargeables par variable d'environnement / secret Streamlit (MODEL_NAME,
# EMBEDDING_MODEL) : permet de basculer l'app sur un modèle autorisé par le
# compte sans redéployer le code.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mistral-embed")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral-small-latest")
MODEL_TEMPERATURE = 0.1
MODEL_MAX_TOKENS = 1200

# %% INPUT PATHS -----
INPUT_DIR = "inputs"
CASES_PATH = Path("eval_cases/nba_eval_cases.yaml")

# %% INDEX PATHS -----
VECTOR_DB_DIR = "vector_db"
FAISS_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "faiss_index.idx")
DOCUMENT_CHUNKS_FILE = os.path.join(VECTOR_DB_DIR, "document_chunks.pkl")

# %% EMBEDDING -----
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
EMBEDDING_BATCH_SIZE = 32

# %% SEARCH -----
SEARCH_K = 5
RETRIEVAL_STRATEGY = "hybrid"  # faiss
SQL_FALLBACK_TO_FAISS = True
SQL_ROUTE_KEYWORDS = [
    "meilleur",
    "meilleurs",
    "top",
    "classement",
    "plus grand",
    "plus haut",
    "plus faible",
    "combien",
    "moyenne",
    "total",
    "totaux",
    "pourcentage",
    "ratio",
    "compare",
    "comparaison",
]
SQL_ROUTE_METRICS = [
    "pts",
    "points",
    "fgm",
    "fga",
    "fg%",
    "3pa",
    "3p%",
    "3 points",
    "trois points",
    "three_p_pct",
    "ftm",
    "fta",
    "ft%",
    "lancers francs",
    "oreb",
    "dreb",
    "reb",
    "rebonds",
    "passes decisives",
    "passes décisives",
    "assists",
    "ast",
    "stl",
    "interceptions",
    "blk",
    "contres",
    "tov",
    "turnovers",
    "pf",
    "fautes personnelles",
    "fp",
    "fantasy points",
    "dd2",
    "double-double",
    "td3",
    "triple-double",
    "+/-",
    "plus-minus",
    "offrtg",
    "defrtg",
    "netrtg",
    "ast%",
    "ast/to",
    "ast ratio",
    "oreb%",
    "dreb%",
    "reb%",
    "to ratio",
    "efg%",
    "ts%",
    "usg%",
    "pace",
    "pie",
    "poss",
    "possessions",
]
INDEX_VERSION = "faiss_v1"

# %% EVALUATION -----
EVAL_MAX_CONCURRENCY = 1
PROMPT_VERSION = "v1"
RAGAS_ANSWER_RELEVANCY_STRICTNESS = 3

# %% DATABASE -----
DATABASE_DIR = "database"
DATABASE_FILE = "database/nba.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# %% APPLICATION -----
APP_TITLE = "NBA Analyst AI"
NAME = "NBA"
