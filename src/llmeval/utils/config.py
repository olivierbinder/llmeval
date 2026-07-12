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
EMBEDDING_MODEL = "mistral-embed"
MODEL_NAME = "mistral-small-latest"  # mistral-large-latest
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
RETRIEVAL_STRATEGY = "faiss"
INDEX_VERSION = "faiss_v1"

# %% EVALUATION -----
EVAL_MAX_CONCURRENCY = 1
PROMPT_VERSION = "v1"
RAGAS_ANSWER_RELEVANCY_STRICTNESS = 3

# %% DATABASE -----
DATABASE_DIR = "database"
DATABASE_FILE = os.path.join(DATABASE_DIR, "interactions.db")
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# %% APPLICATION -----
APP_TITLE = "NBA Analyst AI"
NAME = "NBA"
