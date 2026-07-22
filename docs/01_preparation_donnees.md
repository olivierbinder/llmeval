# Préparation des données

<div class="lead-callout">
Des sources hétérogènes sont transformées en deux supports interrogeables : un index vectoriel FAISS et une base SQLite.
</div>

## Sources utilisées

- Discussions Reddit NBA en PDF. (autres documents exploitables par le loader)
- Classeur Excel `regular NBA.xlsx`.
- Cas d’évaluation manuels en YAML.

## Chaîne de préparation

```mermaid
%%{init: {"themeVariables": {"fontSize": "30px"}, "flowchart": {"nodeSpacing": 55, "rankSpacing": 70}} }%%
flowchart LR
    PDF[PDF Reddit] --> LOAD[Parsing documents]
    EXCEL[Excel NBA] --> LOAD
    EXCEL --> DBLOAD[Chargement Excel]
    LOAD --> SPLIT[Découpage chunks]
    SPLIT --> EMB[Embeddings Mistral]
    EMB --> FAISS[Index FAISS]

    DBLOAD --> DB[SQLite nba.db]

    YAML[Questions de test] --> EVAL[Évaluation]
```

## Index vectoriel

| Étape | Fonctions / outils |
| --- | --- |
| Parsing documents | `load_and_parse_files(...)` <br>`PyMuPDF`, `EasyOCR`,  `pandas` |
| Découpage chunks | `VectorStoreManager._split_documents_to_chunks(...)` <br>`RecursiveCharacterTextSplitter` <br>`chunk_size=1500`, `chunk_overlap=150`, `add_start_index=True` |
| Embeddings Mistral | `VectorStoreManager._generate_embeddings(...)` <br>`mistral_client.embeddings.create(...)` <br>modèle `mistral-embed`, batch `32`, vecteurs `1024` dimensions |
| Index FAISS | `VectorStoreManager.build_index(...)` <br>`faiss.normalize_L2(...)`, `faiss.IndexFlatIP` <br>similarité cosinus via produit scalaire, `302` chunks indexés |

`src/llmeval/scripts/indexer.py` orchestre ces étapes à partir du dossier `inputs/`.

Sorties principales :

- `vector_db/faiss_index.idx` ;
- `vector_db/document_chunks.pkl`.

## Base structurée

| Étape | Fonctions / outils |
| --- | --- |
| Lecture Excel | `read_teams(...)`, `read_features(...)`, `read_players(...)` <br>`pandas.read_excel(...)` <br>feuilles `Equipe`, `Dictionnaire des données`, `Données NBA` |
| Normalisation | `normalize_column_name(...)`, `clean_column_label(...)` <br>renommage des colonnes NBA vers des noms SQL stables |
| Validation | `TeamImport`, `FeatureImport`, `PlayerImport` <br>`Pydantic`, `extra="forbid"`, `45` colonnes joueurs attendues |
| Création SQLite | `recreate_database(...)`, `create_tables(...)` <br>`SQLAlchemy ORM`, tables `teams`, `features`, `players` |
| Insertion + contrôles | `insert_data(...)`, `run_checks(...)` <br>contrôle des volumes, équipes inconnues, doublons joueur/équipe |

`src/llmeval/ingestion/load_excel_to_db.py` orchestre le chargement du classeur `inputs/regular NBA.xlsx`.

Sortie principale :

- `database/nba.db` : `30` équipes, `45` features, `569` joueurs.

## Cas d’évaluation

| Champ | Rôle |
| --- | --- |
| `id` | Identifiant stable du cas |
| `category` | Type de question évaluée |
| `source_type` | Source principale : Reddit ou Excel |
| `question` | Question envoyée au système |
| `reference_answer` | Réponse attendue pour l’évaluation |
| `expected_behavior` | Comportement cible : répondre, synthétiser, refuser |
| `expected_sources` | Sources qui doivent justifier la réponse |
| `evidence_notes` | Notes de validation manuelle |

| Cas | Catégorie | Question |
| --- | --- | --- |
| `Q01` | `qualitative_simple` | Qu'est-ce qui rend Julius Randle plus convaincant dans ces playoffs selon les commentaires ? |
| `Q02` | `qualitative_simple` | Pourquoi les Timberwolves impressionnent-ils certains fans dans le fil Reddit ? |
| `Q03` | `qualitative_comparison` | Quelles équipes reviennent le plus souvent comme surprises positives en playoffs, et pour quelles raisons ? |
| `Q04` | `qualitative_complex` | Pourquoi les Pacers peuvent-ils être sous-estimés par le public national selon Reddit ? |
| `Q05` | `qualitative_noisy` | Franchement, OKC-Indiana en Finales, c'est vraiment le truc soporifique que certains annoncent ? |
| `Q06` | `historical_analysis` | Sur quoi repose l'argument statistique en faveur de Reggie Miller en playoffs ? |
| `Q07` | `historical_qa` | Une équipe NBA a-t-elle déjà eu l'avantage du terrain seulement à partir des Finales ? |
| `Q08` | `quantitative_excel` | Parmi les joueurs avec au moins 300 tirs à trois points tentés, qui a le meilleur pourcentage ? |
| `Q09` | `quantitative_excel` | Quel joueur possède le plus grand total de rebonds dans la table des joueurs ? |
| `Q10` | `quantitative_limit` | Qui a le meilleur pourcentage à trois points sur ses cinq derniers matchs ? |

`eval_cases/nba_eval_cases.yaml` sert de contrat d’évaluation reproductible.
