# Evaluation RAGAS - nba_rag_eval_baseline v2

**Experience** : `pydantic_ai_constrained_rag`

## Scores moyens

| Metrique | Score moyen |
|---|---:|
| faithfulness | 0.773 |
| answer_relevancy | 0.320 |
| context_precision | 0.679 |
| context_recall | 0.393 |

## Scores par categorie

| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1.000 | 0.899 | 1.000 | 0.500 | 1 |
| historical_qa | 0.333 | n/a | n/a | n/a | 1 |
| qualitative_comparison | n/a | n/a | n/a | n/a | 1 |
| qualitative_complex | 1.000 | 0.819 | 1.000 | 0.000 | 1 |
| qualitative_noisy | 1.000 | 0.000 | 1.000 | 1.000 | 1 |
| qualitative_simple | 0.800 | 0.422 | 0.750 | 0.500 | 2 |
| quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | 2 |
| quantitative_limit | 0.250 | 0.000 | 1.000 | 0.750 | 1 |

## Cas evalues

| Cas | Categorie | Confiance | Contexte insuffisant | Sources attendues | Sources utilisees | Sources retrouvees |
|---|---|---|---:|---|---|---|
| Q01 | qualitative_simple | medium | False | Reddit 1.pdf | Reddit 1.pdf | Reddit 1.pdf; Reddit 2.pdf |
| Q02 | qualitative_simple | high | False | Reddit 1.pdf | Reddit 1.pdf | Reddit 1.pdf |
| Q03 | qualitative_comparison | high | False | Reddit 1.pdf | Reddit 1.pdf | Reddit 1.pdf |
| Q04 | qualitative_complex | high | False | Reddit 2.pdf | Reddit 2.pdf | Reddit 2.pdf |
| Q05 | qualitative_noisy | medium | False | Reddit 2.pdf | Reddit 2.pdf | Reddit 2.pdf |
| Q06 | historical_analysis | medium | False | Reddit 3.pdf | Reddit 3.pdf | Reddit 3.pdf |
| Q07 | historical_qa | high | False | Reddit 4.pdf | Reddit 4.pdf | Reddit 4.pdf |
| Q08 | quantitative_excel | low | True | regular NBA.xlsx (Feuille: Données NBA) | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse) | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Analyse); Reddit 3.pdf |
| Q09 | quantitative_excel | low | True | regular NBA.xlsx (Feuille: Données NBA) | regular NBA.xlsx (Feuille: Analyse) | regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Q10 | quantitative_limit | low | True | regular NBA.xlsx (Feuille: Données NBA); regular NBA.xlsx (Feuille: Dictionnaire des données) | n/a | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide) |

## Lecture rapide

- Les cas qualitatifs testent la capacite du RAG texte a retrouver et synthetiser les PDF Reddit.
- Les cas quantitatifs testent les limites de l'Excel indexe comme texte.
- Les champs `confidence`, `insufficient_context` et `used_sources` viennent de la sortie structuree Pydantic AI.
- Le cas Q10 doit rester prudent, car les donnees actuelles ne contiennent pas de split sur les cinq derniers matchs.
