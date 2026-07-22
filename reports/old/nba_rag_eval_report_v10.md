# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_10_short_answers`
- **Version** : `v1`
- **Experience** : `with_sql_strategy`
- **Duree d'execution** : `8min 26s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.875 | 10/10 |
| `answer_relevancy` | 0.694 | 10/10 |
| `context_precision` | 0.689 | 10/10 |
| `context_recall` | 0.722 | 10/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.849 | 0.250 | 0.000 |
| historical_qa | 1 | 1.000 | 0.969 | 1.000 | 0.667 |
| qualitative_comparison | 1 | 1.000 | 0.846 | 0.000 | 0.800 |
| qualitative_complex | 1 | 1.000 | 0.941 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 1.000 | 0.748 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.875 | 0.819 | 1.000 | 0.875 |
| quantitative_excel | 2 | 1.000 | 0.473 | 0.500 | 0.500 |
| quantitative_limit | 1 | 0.000 | 0.000 | 0.639 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | faiss | qualitative_simple | 1.000 | 0.876 | 1.000 | 1.000 | high | 5 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 0.750 | 0.762 | 1.000 | 0.750 | high | 5 | 0 |
| Q03 | evaluated | faiss | qualitative_comparison | 1.000 | 0.846 | 0.000 | 0.800 | medium | 5 | 0 |
| Q04 | evaluated | faiss | qualitative_complex | 1.000 | 0.941 | 1.000 | 1.000 | high | 5 | 0 |
| Q05 | evaluated | faiss | qualitative_noisy | 1.000 | 0.748 | 1.000 | 1.000 | medium | 5 | 0 |
| Q06 | evaluated | faiss | historical_analysis | 1.000 | 0.849 | 0.250 | 0.000 | high | 5 | 0 |
| Q07 | evaluated | faiss | historical_qa | 1.000 | 0.969 | 1.000 | 0.667 | high | 5 | 0 |
| Q08 | evaluated | sql | quantitative_excel | 1.000 | 0.945 | 1.000 | 1.000 | high | 1 | 0 |
| Q09 | evaluated | sql_fallback_faiss | quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q10 | evaluated | sql_fallback_faiss | quantitative_limit | 0.000 | 0.000 | 0.639 | 1.000 | high | 5 | 0 |

## Performance

| Etape | Temps total | Attente | API | Appels juge | Tokens entree | Tokens sortie |
|---|---:|---:|---:|---:|---:|---:|
| Reponses agent | 11.51s | n/a | n/a | 10 | 23882 | 933 |
| RAGAS total | 486.00s | 365.14s | 119.92s | 106 | 141683 | 10933 |

| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 6.29s | 3.66s | 2.61s | 2 | 0 | 3073.3 | 343 |
| Answer relevancy | 18.54s | 15.96s | 2.55s | 3 | 2 | 1462.8 | 94.6 |
| Context precision | 19.06s | 13.90s | 5.12s | 4.6 | 0 | 6387.7 | 449.7 |
| Context recall | 4.71s | 2.99s | 1.71s | 1 | 0 | 3244.5 | 206 |

| Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|
| Q01 | 2 | 5 | 5 | 1 |
| Q02 | 2 | 5 | 5 | 1 |
| Q03 | 2 | 5 | 5 | 1 |
| Q04 | 2 | 5 | 5 | 1 |
| Q05 | 2 | 5 | 5 | 1 |
| Q06 | 2 | 5 | 5 | 1 |
| Q07 | 2 | 5 | 5 | 1 |
| Q08 | 2 | 5 | 1 | 1 |
| Q09 | 2 | 5 | 5 | 1 |
| Q10 | 2 | 5 | 5 | 1 |
