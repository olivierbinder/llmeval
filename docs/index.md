# Mission : évaluer un LLM avec un système RAG

<div class="lead-callout">
Construire un prototype capable de répondre à des questions sur une saison de NBA, puis mesurer la qualité des réponses avec une méthodologie reproductible.
</div>

## Objectif de la soutenance


- Expliquer le fonctionnement du système RAG.
- Montrer comment l’évaluation est orchestrée et observée.
- Présenter le repo Git.

## Vue générale

```mermaid
%%{init: {"themeVariables": {"fontSize": "32px"}, "flowchart": {"nodeSpacing": 55, "rankSpacing": 70}} }%%
flowchart LR
    A[Sources NBA] --> B[Préparation]
    B --> C[Index FAISS]
    B --> D[Base SQLite]
    C --> E[Agent RAG]
    D --> E
    E --> F[Évaluation]
    F --> G[Rapports + Logfire]
```

## Stack principale

[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=for-the-badge&logoColor=white)](https://mistral.ai/)
[![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)

[![RAGAS](https://img.shields.io/badge/RAGAS-00A67E?style=for-the-badge&logoColor=white)](https://docs.ragas.io/)
[![Pydantic AI](https://img.shields.io/badge/Pydantic%20AI-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/)
[![Pydantic Evals](https://img.shields.io/badge/Pydantic%20Evals-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/evals/)
[![Logfire](https://img.shields.io/badge/Logfire-DC2626?style=for-the-badge&logoColor=white)](https://pydantic.dev/logfire)

## Livrables au sein du repo

| Livrable attendu | Dossiers, fichiers |
| --- | --- |
| Environnement reproductible | `pyproject.toml` <br>`uv.lock`&nbsp;[![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logoColor=white)](https://docs.astral.sh/uv/) |
| Préparation des données | `src/llmeval/scripts/indexer.py` --> Orchestrateur <br>`src/llmeval/utils/data_loader.py`&nbsp;[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-306998?style=flat-square&logoColor=white)](https://pymupdf.readthedocs.io/)&nbsp;[![EasyOCR](https://img.shields.io/badge/EasyOCR-111827?style=flat-square&logoColor=white)](https://github.com/JaidedAI/EasyOCR)<br>`src/llmeval/utils/vector_store.py`&nbsp;[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square&logoColor=white)](https://mistral.ai/)<br>`vector_db/`&nbsp;[![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=flat-square&logo=meta&logoColor=white)](https://faiss.ai/)<br>`src/llmeval/ingestion/`&nbsp;[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)<br>`database/nba.db`&nbsp;[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/) |
| Mise en place du RAG | `src/llmeval/utils/rag_agent.py`&nbsp;[![Pydantic AI](https://img.shields.io/badge/Pydantic%20AI-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/)&nbsp;[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square&logoColor=white)](https://mistral.ai/)<br>`src/llmeval/utils/sql_tool.py`&nbsp;[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)&nbsp;[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square&logoColor=white)](https://mistral.ai/)|
| Évaluation et tests | `eval_cases/`<br>`src/llmeval/scripts/evaluate.py`&nbsp;[![Pydantic Evals](https://img.shields.io/badge/Pydantic%20Evals-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/evals/)&nbsp;[![RAGAS](https://img.shields.io/badge/RAGAS-00A67E?style=flat-square&logoColor=white)](https://docs.ragas.io/)&nbsp;[![Mistral](https://img.shields.io/badge/Mistral-FA520F?style=flat-square&logoColor=white)](https://mistral.ai/)<br>`src/llmeval/utils/eval_schemas.py`&nbsp;[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/) |
| Observabilité et rapports | `src/llmeval/utils/logfire_datasets.py`&nbsp;[![Logfire](https://img.shields.io/badge/Logfire-DC2626?style=flat-square&logo=pydantic&logoColor=white)](https://pydantic.dev/logfire)<br>`reports/` |
