# TODO — Evaluation hybride FAISS / SQL

## Objectif

Comparer le pipeline actuel FAISS avec un pipeline hybride utilisant SQL pour les questions structurées, puis fallback FAISS si SQL échoue.

## À coder

1. Configuration
   - Mettre `RETRIEVAL_STRATEGY = "hybrid"` dans `config.py`.
   - Ajouter `SQL_FALLBACK_TO_FAISS = True`.

2. Schémas
   - Ajouter dans `RagAnswer` un champ `retrieval_strategy`.
   - Ajouter un champ optionnel `sql_error_reason`.

3. Evaluation hybride
   - Dans `evaluate.py`, créer un `build_hybrid_task`.
   - Tenter `run_sql_question(question)` pour les questions probablement structurées (heuristique simple basée sur SQL_ROUTE_KEYWORDS et SQL_ROUTE_METRICS)
   - Si SQL réussit : retourner une réponse avec `retrieval_strategy="sql"`.
   - Si SQL échoue : fallback FAISS/RAG avec `retrieval_strategy="sql_fallback_faiss"`.
   - Sinon FAISS direct : `retrieval_strategy="faiss"`.

4. Métriques
   - Si `retrieval_strategy="sql"` : ne pas calculer les métriques RAGAS contextuelles, les marquer `N/A`.
   - Si FAISS ou fallback FAISS : garder les métriques RAGAS actuelles.
   - Enregistrer `retrieval_strategy` et `sql_error_reason` dans les attributs d’éval.

5. Tests
   - Relancer l’évaluation en mode FAISS baseline.
   - Relancer en mode hybride.
   - Vérifier Q08, Q09, Q10.
   - Ajouter 2 ou 3 cas mixtes texte + numérique.

6. Rapport
   - Ajuster en intégrant nouvelles colonnes comme `sql_error_reason` faisant le moins de modifs. On developpera cette partie reports plus tard.
