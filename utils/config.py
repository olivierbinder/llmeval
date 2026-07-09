# %% IMPORTS -----
import os

from dotenv import load_dotenv

# %%   ENVIRONEMENT VARIABLES -----
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    print(
        "⚠️ Attention: La clé API Mistral (MISTRAL_API_KEY) n'est pas définie dans le fichier .env"
    )
    # raise ValueError("Clé API Mistral manquante. Veuillez la définir dans le fichier .env")

# %%  MISTRAL MODEL -----
EMBEDDING_MODEL = "mistral-embed"
MODEL_NAME = "mistral-small-latest"  # mistral-large-latest

# %%  INDEX PATHS -----
INPUT_DIR = "inputs"
VECTOR_DB_DIR = "vector_db"
FAISS_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "faiss_index.idx")
DOCUMENT_CHUNKS_FILE = os.path.join(VECTOR_DB_DIR, "document_chunks.pkl")

# %%  EMBEDDING -----
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
EMBEDDING_BATCH_SIZE = 32

# %%  SEARCH -----
SEARCH_K = 5

# %%  DATABASE -----
DATABASE_DIR = "database"
DATABASE_FILE = os.path.join(DATABASE_DIR, "interactions.db")
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"  # URL pour SQLAlchemy

# %%  APPLICATION -----
APP_TITLE = "NBA Analyst AI"
NAME = "NBA"
