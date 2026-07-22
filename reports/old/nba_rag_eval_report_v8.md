# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_expanded_short_answers`
- **Version** : `v8`
- **Experience** : `with_sql_strategy_short_answers`
- **Duree d'execution** : `16min 12s`
- **Cas evalues** : `20`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.883 | 20/20 |
| `answer_relevancy` | 0.767 | 20/20 |
| `context_precision` | 0.720 | 20/20 |
| `context_recall` | 0.809 | 20/20 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 2 | 0.800 | 0.840 | 0.625 | 0.500 |
| historical_qa | 2 | 1.000 | 0.878 | 0.875 | 0.833 |
| qualitative_comparison | 2 | 0.875 | 0.815 | 0.500 | 0.500 |
| qualitative_complex | 2 | 0.833 | 0.966 | 0.739 | 0.750 |
| qualitative_noisy | 2 | 1.000 | 0.856 | 0.750 | 1.000 |
| qualitative_simple | 4 | 0.787 | 0.895 | 0.701 | 0.754 |
| quantitative_excel | 4 | 1.000 | 0.762 | 1.000 | 1.000 |
| quantitative_limit | 2 | 0.750 | 0.000 | 0.308 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | faiss | qualitative_simple | 0.400 | 0.905 | 0.000 | 0.600 | medium | 5 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 1.000 | 0.868 | 1.000 | 1.000 | high | 5 | 0 |
| Q03 | evaluated | faiss | qualitative_simple | 1.000 | 0.856 | 0.806 | 0.667 | high | 5 | 0 |
| Q04 | evaluated | faiss | qualitative_simple | 0.750 | 0.951 | 1.000 | 0.750 | high | 5 | 0 |
| Q05 | evaluated | faiss | qualitative_comparison | 1.000 | 0.838 | 0.000 | 1.000 | medium | 5 | 0 |
| Q06 | evaluated | sql | qualitative_comparison | 0.750 | 0.791 | 1.000 | 0.000 | high | 1 | 0 |
| Q07 | evaluated | faiss | qualitative_complex | 1.000 | 0.991 | 0.478 | 0.500 | medium | 5 | 0 |
| Q08 | evaluated | faiss | qualitative_complex | 0.667 | 0.941 | 1.000 | 1.000 | high | 5 | 0 |
| Q09 | evaluated | faiss | qualitative_noisy | 1.000 | 0.858 | 1.000 | 1.000 | medium | 5 | 0 |
| Q10 | evaluated | faiss | qualitative_noisy | 1.000 | 0.855 | 0.500 | 1.000 | medium | 5 | 0 |
| Q11 | evaluated | faiss | historical_analysis | 1.000 | 0.850 | 0.250 | 1.000 | high | 5 | 0 |
| Q12 | evaluated | faiss | historical_analysis | 0.600 | 0.830 | 1.000 | 0.000 | high | 5 | 0 |
| Q13 | evaluated | faiss | historical_qa | 1.000 | 0.969 | 1.000 | 0.667 | high | 5 | 0 |
| Q14 | evaluated | faiss | historical_qa | 1.000 | 0.786 | 0.750 | 1.000 | high | 5 | 0 |
| Q15 | evaluated | sql | quantitative_excel | 1.000 | 0.822 | 1.000 | 1.000 | high | 1 | 0 |
| Q16 | evaluated | sql | quantitative_excel | 1.000 | 0.764 | 1.000 | 1.000 | high | 1 | 0 |
| Q17 | evaluated | sql | quantitative_excel | 1.000 | 0.754 | 1.000 | 1.000 | high | 1 | 0 |
| Q18 | evaluated | sql | quantitative_excel | 1.000 | 0.708 | 1.000 | 1.000 | high | 1 | 0 |
| Q19 | evaluated | sql_fallback_faiss | quantitative_limit | 1.000 | 0.000 | 0.417 | 1.000 | low | 5 | 0 |
| Q20 | evaluated | sql_fallback_faiss | quantitative_limit | 0.500 | 0.000 | 0.200 | 1.000 | low | 5 | 0 |

## Performance

| Etape | Temps total | Attente | API | Appels juge | Tokens entree | Tokens sortie |
|---|---:|---:|---:|---:|---:|---:|
| Reponses agent | 32.81s | n/a | n/a | 20 | 41382 | 1585 |
| RAGAS total | 928.11s | 692.19s | 233.86s | 200 | 259943 | 22209 |

| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 6.68s | 3.63s | 3.03s | 2 | n/a | 2883.2 | 406.3 |
| Answer relevancy | 18.23s | 15.76s | 2.43s | 3 | n/a | 1475.7 | 95.2 |
| Context precision | 16.65s | 12.24s | 4.38s | 4 | n/a | 5600.1 | 380.2 |
| Context recall | 4.85s | 2.98s | 1.86s | 1 | n/a | 3038.2 | 228.8 |

| Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|
| Q01 | 2 | 3 | 5 | 1 |
| Q02 | 2 | 3 | 5 | 1 |
| Q03 | 2 | 3 | 5 | 1 |
| Q04 | 2 | 3 | 5 | 1 |
| Q05 | 2 | 3 | 5 | 1 |
| Q06 | 2 | 3 | 1 | 1 |
| Q07 | 2 | 3 | 5 | 1 |
| Q08 | 2 | 3 | 5 | 1 |
| Q09 | 2 | 3 | 5 | 1 |
| Q10 | 2 | 3 | 5 | 1 |
| Q11 | 2 | 3 | 5 | 1 |
| Q12 | 2 | 3 | 5 | 1 |
| Q13 | 2 | 3 | 5 | 1 |
| Q14 | 2 | 3 | 5 | 1 |
| Q15 | 2 | 3 | 1 | 1 |
| Q16 | 2 | 3 | 1 | 1 |
| Q17 | 2 | 3 | 1 | 1 |
| Q18 | 2 | 3 | 1 | 1 |
| Q19 | 2 | 3 | 5 | 1 |
| Q20 | 2 | 3 | 5 | 1 |
