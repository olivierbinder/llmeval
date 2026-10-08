# llmeval

`llmeval` est un prototype d'évaluation d'un assistant NBA basé sur un système RAG.

Le projet construit une base de connaissances à partir de documents NBA, interroge ces données avec un agent LLM, puis mesure la qualité des réponses sur un jeu de questions de référence.

## Vue d'ensemble

Le pipeline couvre quatre étapes principales :

1. Charger des sources NBA, notamment des PDFs, fichiers texte, CSV, DOCX et classeurs Excel.
2. Indexer les contenus textuels dans un index vectoriel FAISS avec des embeddings Mistral.
3. Répondre à des questions en français via un agent RAG, avec une stratégie hybride possible : recherche vectorielle et outil SQL pour les questions quantitatives.
4. Évaluer les réponses avec `pydantic-evals`, RAGAS et Logfire, puis générer des rapports Markdown et CSV.

## Données manipulées

Le projet travaille principalement sur :

- des discussions Reddit NBA transformées en documents interrogeables ;
- un fichier Excel de statistiques NBA chargé dans une base SQLite ;
- des cas d'évaluation manuels décrivant les réponses attendues.

## Objectif

L'objectif est de comparer et améliorer la capacité d'un assistant NBA à :

- retrouver les bons contextes ;
- répondre de manière concise et sourcée ;
- traiter des questions qualitatives issues de documents ;
- traiter des questions quantitatives à partir de données structurées ;
- suivre les métriques de qualité, coût, latence et usage des modèles.

## Principaux dossiers

- `src/llmeval/` : code du pipeline, de l'agent, de l'indexation, de l'ingestion SQL et des rapports.
- `app/` : application Streamlit (assistant NBA + consultation des rapports).
- `eval_cases/` : jeux de questions d'évaluation.
- `database/` : base SQLite et documentation utile à l'agent SQL.
- `reports/` : rapports produits par les runs d'évaluation.
- `tests/` : tests du routage SQL/FAISS partagé entre l'évaluation et l'application.

## Application Streamlit

```bash
uv run streamlit run app/streamlit_app.py
```

L'app expose l'assistant NBA (recherche vectorielle FAISS, outil SQL pour les
questions chiffrées) avec les sources, la stratégie utilisée, les métriques de
latence/tokens et une seconde vue qui affiche les rapports d'évaluation déjà
versionnés.

Secrets attendus (`.streamlit/secrets.toml` en local, secrets de l'app sur
Streamlit Cloud) :

| Clé | Rôle |
| --- | --- |
| `MISTRAL_API_KEY` | obligatoire (embeddings + génération) |
| `MODEL_NAME` | modèle de génération, défaut `mistral-small-latest` (ex. `ministral-8b-latest` si ton compte n'a pas de quota sur le modèle par défaut) |
| `EMBEDDING_MODEL` | modèle d'embeddings, défaut `mistral-embed` |
| `APP_PASSWORD` | mot de passe d'accès à l'app |
| `QUESTION_LIMIT` | quota de questions par session (défaut `20`) |
| `LOGFIRE_API_KEY` / `LOGFIRE_TOKEN` | optionnel, active les traces Logfire |

Pour vérifier le quota d'un modèle avant de le choisir, l'API renvoie dans ses
en-têtes `x-ratelimit-limit-req-minute` : une valeur `0` signifie que le compte
n'est pas autorisé à utiliser ce modèle (`429 rate_limited`, code `1300`).

### Déploiement Streamlit Community Cloud

1. Pousser le dépôt sur GitHub (repo public).
2. Sur [share.streamlit.io](https://share.streamlit.io), créer une app avec le
   fichier principal `app/streamlit_app.py`.
3. Dans *Advanced settings*, choisir Python 3.12 et coller les secrets ci-dessus.
4. Déployer.

`app/requirements.txt` est volontairement minimal (pas d'`easyocr`/`torch`, pas
de `ragas`/`pydantic-evals`) et sert de fichier de dépendances au déploiement :
il est placé dans le dossier de l'entrypoint, donc prioritaire sur le `uv.lock`
de la racine. L'index FAISS (`vector_db/`), les chunks et la base
(`database/nba.db`) sont versionnés (~1,9 Mo) pour que l'app démarre sans étape
d'ingestion. Si le log de build montre malgré tout un `uv sync`, retirer
`uv.lock` du dépôt (`git rm --cached uv.lock`) et redéployer.

## Tests et qualité

```bash
uv run pytest tests -q
uv run ruff check src app tests
```

