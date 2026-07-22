# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_10_short_answers`
- **Version** : `v1`
- **Experience** : `with_sql_strategy`
- **Duree d'execution** : `8min 14s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.875 | 10/10 |
| `answer_relevancy` | 0.825 | 10/10 |
| `context_precision` | 0.762 | 10/10 |
| `context_recall` | 0.742 | 10/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.830 | 0.250 | 0.000 |
| historical_qa | 1 | 1.000 | 0.969 | 0.950 | 0.667 |
| qualitative_comparison | 1 | 0.500 | 0.851 | 0.000 | 0.000 |
| qualitative_complex | 1 | 1.000 | 0.943 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 1.000 | 0.917 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.875 | 0.913 | 1.000 | 0.875 |
| quantitative_excel | 2 | 1.000 | 0.956 | 1.000 | 1.000 |
| quantitative_limit | 1 | 0.500 | 0.000 | 0.417 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | faiss | qualitative_simple | 1.000 | 0.875 | 1.000 | 1.000 | high | 5 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 0.750 | 0.951 | 1.000 | 0.750 | high | 5 | 0 |
| Q03 | evaluated | faiss | qualitative_comparison | 0.500 | 0.851 | 0.000 | 0.000 | medium | 5 | 0 |
| Q04 | evaluated | faiss | qualitative_complex | 1.000 | 0.943 | 1.000 | 1.000 | high | 5 | 0 |
| Q05 | evaluated | faiss | qualitative_noisy | 1.000 | 0.917 | 1.000 | 1.000 | medium | 5 | 0 |
| Q06 | evaluated | faiss | historical_analysis | 1.000 | 0.830 | 0.250 | 0.000 | high | 5 | 0 |
| Q07 | evaluated | faiss | historical_qa | 1.000 | 0.969 | 0.950 | 0.667 | high | 5 | 0 |
| Q08 | evaluated | sql | quantitative_excel | 1.000 | 0.964 | 1.000 | 1.000 | high | 1 | 0 |
| Q09 | evaluated | sql | quantitative_excel | 1.000 | 0.947 | 1.000 | 1.000 | high | 1 | 0 |
| Q10 | evaluated | sql_fallback_faiss | quantitative_limit | 0.500 | 0.000 | 0.417 | 1.000 | low | 5 | 0 |

## Performance

| Etape | Temps total | Attente | API | Appels LLM | Tokens entree | Tokens sortie |
|---|---:|---:|---:|---:|---:|---:|
| Reponses agent | 21.59s | n/a | 21.24s | 24 | 45896 | 1668 |
| RAGAS total | 469.85s | 344.37s | 124.58s | 102 | 134909 | 10822 |

| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 6.45s | 3.55s | 2.89s | 2 | 0 | 2975.9 | 356.5 |
| Answer relevancy | 18.67s | 15.84s | 2.79s | 3 | 2 | 1464.6 | 101.6 |
| Context precision | 17.21s | 12.14s | 5.04s | 4.2 | 0 | 5904.6 | 413 |
| Context recall | 4.65s | 2.90s | 1.73s | 1 | 0 | 3145.8 | 211.1 |

Nombre d'appels API

| Cas | Reponse agent | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Q01 | 1 | 2 | 5 | 5 | 1 |
| Q02 | 1 | 2 | 5 | 5 | 1 |
| Q03 | 1 | 2 | 5 | 5 | 1 |
| Q04 | 1 | 2 | 5 | 5 | 1 |
| Q05 | 1 | 2 | 5 | 5 | 1 |
| Q06 | 1 | 2 | 5 | 5 | 1 |
| Q07 | 1 | 2 | 5 | 5 | 1 |
| Q08 | 5 | 2 | 5 | 1 | 1 |
| Q09 | 5 | 2 | 5 | 1 | 1 |
| Q10 | 7 | 2 | 5 | 5 | 1 |
