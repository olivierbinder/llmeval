# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_baseline`
- **Version** : `v7`
- **Experience** : `with_sql_strategy`
- **Duree d'execution** : `7min 7s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.846 | 8/10 |
| `answer_relevancy` | 0.883 | 8/10 |
| `context_precision` | 0.788 | 8/10 |
| `context_recall` | 0.938 | 8/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.872 | 1.000 | 0.500 |
| historical_qa | 1 | 0.750 | 0.802 | 0.804 | 1.000 |
| qualitative_comparison | 1 | 0.600 | 0.983 | 0.250 | 1.000 |
| qualitative_complex | 1 | 1.000 | 0.993 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 1.000 | 0.797 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.833 | 0.902 | 0.625 | 1.000 |
| quantitative_excel | 2 | n/a | n/a | n/a | n/a |
| quantitative_limit | 1 | 0.750 | 0.810 | 1.000 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q07 | evaluated | faiss | historical_qa | 0.750 | 0.802 | 0.804 | 1.000 | high | 5.0 | 0 |
| Q08 | evaluated | sql | quantitative_excel | n/a | n/a | n/a | n/a | high | n/a | 0 |
| Q09 | evaluated | sql | quantitative_excel | n/a | n/a | n/a | n/a | high | n/a | 0 |
| Q10 | evaluated | sql_fallback_faiss | quantitative_limit | 0.750 | 0.810 | 1.000 | 1.000 | low | 5.0 | 0 |
| Q01 | evaluated | faiss | qualitative_simple | 0.667 | 0.864 | 0.250 | 1.000 | medium | 5.0 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 1.000 | 0.940 | 1.000 | 1.000 | high | 5.0 | 0 |
| Q03 | evaluated | faiss | qualitative_comparison | 0.600 | 0.983 | 0.250 | 1.000 | high | 5.0 | 0 |
| Q04 | evaluated | faiss | qualitative_complex | 1.000 | 0.993 | 1.000 | 1.000 | high | 5.0 | 0 |
| Q05 | evaluated | faiss | qualitative_noisy | 1.000 | 0.797 | 1.000 | 1.000 | medium | 5.0 | 0 |
| Q06 | evaluated | faiss | historical_analysis | 1.000 | 0.872 | 1.000 | 0.500 | medium | 5.0 | 0 |
