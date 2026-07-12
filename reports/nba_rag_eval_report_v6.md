# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_baseline`
- **Version** : `v6`
- **Experience** : `pydantic_evals_refactor`
- **Duree d'execution** : `8min 42s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.702 | 10/10 |
| `answer_relevancy` | 0.623 | 10/10 |
| `context_precision` | 0.564 | 10/10 |
| `context_recall` | 0.750 | 10/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 0.857 | 0.895 | 1.000 | 0.500 |
| historical_qa | 1 | 0.750 | 0.802 | 0.804 | 1.000 |
| qualitative_comparison | 1 | 0.400 | 0.987 | 0.417 | 1.000 |
| qualitative_complex | 1 | 1.000 | 0.986 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 1.000 | 0.779 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.757 | 0.891 | 0.708 | 1.000 |
| quantitative_excel | 2 | 0.500 | 0.000 | 0.000 | 0.000 |
| quantitative_limit | 1 | 0.500 | 0.000 | 0.000 | 1.000 |

## Synthese des cas

| Cas | Statut | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | qualitative_simple | 0.714 | 0.887 | 0.417 | 1.000 | medium | 5 | 0 |
| Q02 | evaluated | qualitative_simple | 0.800 | 0.896 | 1.000 | 1.000 | high | 5 | 0 |
| Q03 | evaluated | qualitative_comparison | 0.400 | 0.987 | 0.417 | 1.000 | high | 5 | 0 |
| Q04 | evaluated | qualitative_complex | 1.000 | 0.986 | 1.000 | 1.000 | high | 5 | 0 |
| Q05 | evaluated | qualitative_noisy | 1.000 | 0.779 | 1.000 | 1.000 | medium | 5 | 0 |
| Q06 | evaluated | historical_analysis | 0.857 | 0.895 | 1.000 | 0.500 | medium | 5 | 0 |
| Q07 | evaluated | historical_qa | 0.750 | 0.802 | 0.804 | 1.000 | high | 5 | 0 |
| Q08 | evaluated | quantitative_excel | 0.000 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q09 | evaluated | quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q10 | evaluated | quantitative_limit | 0.500 | 0.000 | 0.000 | 1.000 | low | 5 | 0 |
