# Migration Pydantic Evals + RAGAS 0.4

## Application

Le patch est prévu pour être appliqué depuis la racine du projet :

```bash
git apply llmeval_pydantic_evals.patch
uv sync --frozen
uv run evaluate
```

L'archive contient les fichiers réécrits. Si vous les copiez manuellement, supprimez aussi :

```text
src/llmeval/utils/reports.py
```

## Architecture retenue

- Pydantic Evals orchestre le dataset, les cas, la tâche, l'expérience et le rapport.
- Un seul `RagasEvaluator` expose quatre scores : `faithfulness`, `answer_relevancy`, `context_precision` et `context_recall`.
- RAGAS utilise son API moderne `metrics.collections`, `llm_factory()` et `ascore()`.
- Les métadonnées d'expérience, attributs de retrieval et métriques sont transmis à Pydantic Evals / Logfire.
- Les anciens wrappers RAGAS, la boucle `ragas.evaluate()` et le reporting CSV/Markdown sont supprimés.

## Dépendance transitive verrouillée

`langchain-community` est borné à `>=0.4.1,<0.4.2` : RAGAS 0.4.3 importe encore `langchain_community.chat_models.vertexai`, retiré de la version 0.4.2.

## Vérifications effectuées

- `uv lock --check`
- compilation Python de tout `src/`
- `ruff check src`
- chargement des 10 cas YAML
- sérialisation du dataset et du `RagasEvaluator`
- exécution complète Pydantic Evals avec les quatre métriques simulées
- initialisation de `RagAgent`, `VectorStoreManager` et de la tâche

Aucun appel API Mistral réel n'a été lancé pendant les tests. Le test réel nécessite votre clé et vos fichiers `vector_db/`.
