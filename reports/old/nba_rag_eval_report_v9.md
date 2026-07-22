# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_balanced_short_answers`
- **Version** : `v9`
- **Experience** : `with_sql_strategy_short_answers`
- **Duree d'execution** : `7min 38s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.950 | 9/10 |
| `answer_relevancy` | 0.794 | 9/10 |
| `context_precision` | 0.750 | 9/10 |
| `context_recall` | 0.880 | 9/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.855 | 0.417 | 1.000 |
| historical_qa | 1 | 1.000 | 0.969 | 1.000 | 0.667 |
| qualitative_comparison | 1 | 1.000 | 0.846 | 0.000 | 1.000 |
| qualitative_complex | 1 | 1.000 | 0.941 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 0.750 | 0.914 | 1.000 | 1.000 |
| qualitative_simple | 2 | 0.900 | 0.823 | 1.000 | 0.625 |
| quantitative_excel | 2 | 1.000 | 0.972 | 1.000 | 1.000 |
| quantitative_limit | 1 | 1.000 | 0.000 | 0.333 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | faiss | qualitative_simple | 1.000 | 0.873 | 1.000 | 1.000 | high | 5.0 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 0.800 | 0.772 | 1.000 | 0.250 | high | 5.0 | 0 |
| Q03 | evaluated | faiss | qualitative_comparison | 1.000 | 0.846 | 0.000 | 1.000 | medium | 5.0 | 0 |
| Q04 | evaluated | faiss | qualitative_complex | 1.000 | 0.941 | 1.000 | 1.000 | high | 5.0 | 0 |
| Q05 | evaluated | faiss | qualitative_noisy | 0.750 | 0.914 | 1.000 | 1.000 | medium | 5.0 | 0 |
| Q06 | evaluated | faiss | historical_analysis | 1.000 | 0.855 | 0.417 | 1.000 | high | 5.0 | 0 |
| Q07 | evaluated | faiss | historical_qa | 1.000 | 0.969 | 1.000 | 0.667 | high | 5.0 | 0 |
| Q08 | evaluated | sql | quantitative_excel | n/a | n/a | n/a | n/a | high | n/a | 0 |
| Q09 | evaluated | sql | quantitative_excel | 1.000 | 0.972 | 1.000 | 1.000 | high | 1.0 | 0 |
| Q10 | evaluated | sql_fallback_faiss | quantitative_limit | 1.000 | 0.000 | 0.333 | 1.000 | low | 5.0 | 0 |

## Performance

| Etape | Temps total | Attente | API | Appels juge | Tokens entree | Tokens sortie |
|---|---:|---:|---:|---:|---:|---:|
| Reponses agent | 15.32s | n/a | n/a | 10 | 22178 | 796 |
| RAGAS total | 437.53s | 323.44s | 113.19s | 95 | 129479 | 10265 |

| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 6.64s | 3.66s | 2.97s | 2 | 0 | 3161.2 | 371.3 |
| Answer relevancy | 18.10s | 15.45s | 2.62s | 3 | 2 | 1456.3 | 92.8 |
| Context precision | 19.15s | 13.97s | 5.15s | 4.6 | 0 | 6437.7 | 448.1 |
| Context recall | 4.72s | 2.87s | 1.85s | 1 | 0 | 3331.3 | 228.3 |

| Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|
| Q01 | 2 | 5 | 5 | 1 |
| Q02 | 2 | 5 | 5 | 1 |
| Q03 | 2 | 5 | 5 | 1 |
| Q04 | 2 | 5 | 5 | 1 |
| Q05 | 2 | 5 | 5 | 1 |
| Q06 | 2 | 5 | 5 | 1 |
| Q07 | 2 | 5 | 5 | 1 |
| Q08 | n/a | n/a | n/a | n/a |
| Q09 | 2 | 5 | 1 | 1 |
| Q10 | 2 | 5 | 5 | 1 |
