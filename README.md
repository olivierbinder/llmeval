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
- `eval_cases/` : jeux de questions d'évaluation.
- `database/` : base SQLite et documentation utile à l'agent SQL.
- `reports/` : rapports produits par les runs d'évaluation.

