# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_baseline`
- **Version** : `v5`
- **Experience** : `pydantic_ai_constrained_rag_observability`
- **Duree d'execution** : `8min 46s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.701 | 10/10 |
| `answer_relevancy` | 0.596 | 10/10 |
| `context_precision` | 0.589 | 10/10 |
| `context_recall` | 0.750 | 10/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.872 | 1.000 | 0.500 |
| historical_qa | 1 | 0.750 | 0.834 | 0.804 | 1.000 |
| qualitative_comparison | 1 | 0.600 | 0.831 | 0.417 | 1.000 |
| qualitative_complex | 1 | 0.857 | 0.986 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 1.000 | 0.746 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.817 | 0.847 | 0.708 | 1.000 |
| quantitative_excel | 2 | 0.333 | 0.000 | 0.000 | 0.000 |
| quantitative_limit | 1 | 0.500 | 0.000 | 0.250 | 1.000 |

## Synthese des cas

| Cas | Statut | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | qualitative_simple | 0.833 | 0.886 | 0.417 | 1.000 | medium | 5 | 0 |
| Q02 | evaluated | qualitative_simple | 0.800 | 0.808 | 1.000 | 1.000 | high | 5 | 0 |
| Q03 | evaluated | qualitative_comparison | 0.600 | 0.831 | 0.417 | 1.000 | high | 5 | 0 |
| Q04 | evaluated | qualitative_complex | 0.857 | 0.986 | 1.000 | 1.000 | high | 5 | 0 |
| Q05 | evaluated | qualitative_noisy | 1.000 | 0.746 | 1.000 | 1.000 | medium | 5 | 0 |
| Q06 | evaluated | historical_analysis | 1.000 | 0.872 | 1.000 | 0.500 | medium | 5 | 0 |
| Q07 | evaluated | historical_qa | 0.750 | 0.834 | 0.804 | 1.000 | high | 5 | 0 |
| Q08 | evaluated | quantitative_excel | 0.000 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q09 | evaluated | quantitative_excel | 0.667 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q10 | evaluated | quantitative_limit | 0.500 | 0.000 | 0.250 | 1.000 | low | 5 | 0 |
