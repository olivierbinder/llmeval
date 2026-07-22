# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_10_short_answers`
- **Version** : `v0`
- **Experience** : `faiss only`
- **Duree d'execution** : `9min 9s`
- **Cas evalues** : `10`
- **Task failures** : `0`
- **Evaluator failures** : `0`

## Scores moyens

| Metrique | Score moyen | Couverture |
|---|---:|---:|
| `faithfulness` | 0.817 | 10/10 |
| `answer_relevancy` | 0.611 | 10/10 |
| `context_precision` | 0.642 | 10/10 |
| `context_recall` | 0.542 | 10/10 |

## Scores par categorie

| Categorie | Cas | Faithfulness | Relevancy | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1 | 1.000 | 0.845 | 0.639 | 1.000 |
| historical_qa | 1 | 1.000 | 0.969 | 1.000 | 0.667 |
| qualitative_comparison | 1 | 1.000 | 0.851 | 0.000 | 0.000 |
| qualitative_complex | 1 | 0.667 | 0.943 | 1.000 | 1.000 |
| qualitative_noisy | 1 | 0.750 | 0.858 | 1.000 | 0.000 |
| qualitative_simple | 2 | 0.875 | 0.821 | 1.000 | 0.875 |
| quantitative_excel | 2 | 0.500 | 0.000 | 0.100 | 0.000 |
| quantitative_limit | 1 | 1.000 | 0.000 | 0.583 | 1.000 |

## Synthese des cas

| Cas | Statut | Strategie | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contextes | Erreurs evaluator |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|
| Q01 | evaluated | faiss | qualitative_simple | 1.000 | 0.879 | 1.000 | 1.000 | high | 5 | 0 |
| Q02 | evaluated | faiss | qualitative_simple | 0.750 | 0.763 | 1.000 | 0.750 | high | 5 | 0 |
| Q03 | evaluated | faiss | qualitative_comparison | 1.000 | 0.851 | 0.000 | 0.000 | medium | 5 | 0 |
| Q04 | evaluated | faiss | qualitative_complex | 0.667 | 0.943 | 1.000 | 1.000 | high | 5 | 0 |
| Q05 | evaluated | faiss | qualitative_noisy | 0.750 | 0.858 | 1.000 | 0.000 | medium | 5 | 0 |
| Q06 | evaluated | faiss | historical_analysis | 1.000 | 0.845 | 0.639 | 1.000 | high | 5 | 0 |
| Q07 | evaluated | faiss | historical_qa | 1.000 | 0.969 | 1.000 | 0.667 | high | 5 | 0 |
| Q08 | evaluated | faiss | quantitative_excel | 0.000 | 0.000 | 0.200 | 0.000 | low | 5 | 0 |
| Q09 | evaluated | faiss | quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | low | 5 | 0 |
| Q10 | evaluated | faiss | quantitative_limit | 1.000 | 0.000 | 0.583 | 1.000 | low | 5 | 0 |

## Performance

| Etape | Temps total | Attente | API | Appels LLM | Tokens entree | Tokens sortie |
|---|---:|---:|---:|---:|---:|---:|
| Reponses agent | 11.19s | n/a | 11.19s | 10 | 25879 | 948 |
| RAGAS total | 529.57s | 363.87s | 164.77s | 110 | 148993 | 11284 |

| Metrique RAGAS | Temps/cas | Attente/cas | API/cas | Appels juge/cas | Appels embedding/cas | Tokens entree/cas | Tokens sortie/cas |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 6.86s | 3.49s | 3.36s | 2 | 0 | 3183.9 | 328.2 |
| Answer relevancy | 18.19s | 15.87s | 2.28s | 3 | 2 | 1445.4 | 96.2 |
| Context precision | 23.41s | 14.48s | 8.90s | 5 | 0 | 6901.6 | 483.6 |
| Context recall | 4.49s | 2.55s | 1.94s | 1 | 0 | 3368.4 | 220.4 |

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
| Q08 | 1 | 2 | 5 | 5 | 1 |
| Q09 | 1 | 2 | 5 | 5 | 1 |
| Q10 | 1 | 2 | 5 | 5 | 1 |
