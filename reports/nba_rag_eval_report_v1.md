# Evaluation RAGAS - phase 1

## Scores moyens

| Metrique | Score moyen |
|---|---:|
| faithfulness | 0.762 |
| answer_relevancy | 0.673 |
| context_precision | 0.661 |
| context_recall | 0.660 |

## Scores par categorie

| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 0.636 | 0.876 | 1.000 | 0.500 | 1 |
| historical_qa | 0.393 | 0.799 | 0.804 | 1.000 | 1 |
| qualitative_comparison | 0.875 | 0.835 | 0.250 | 0.600 | 1 |
| qualitative_complex | 0.958 | 0.845 | 1.000 | 1.000 | 1 |
| qualitative_noisy | 0.800 | 0.806 | 1.000 | 1.000 | 1 |
| qualitative_simple | 0.876 | 0.828 | 0.875 | 0.750 | 2 |
| quantitative_excel | 1.000 | 0.455 | 0.000 | 0.000 | 2 |
| quantitative_limit | 0.200 | 0.000 | 0.806 | 1.000 | 1 |

## Cas evalues

| Cas | Categorie | Sources attendues | Sources retrouvees |
|---|---|---|---|
| Q01 | qualitative_simple | Reddit 1.pdf | Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 2.pdf |
| Q02 | qualitative_simple | Reddit 1.pdf | Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf |
| Q03 | qualitative_comparison | Reddit 1.pdf | Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf; Reddit 1.pdf |
| Q04 | qualitative_complex | Reddit 2.pdf | Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf |
| Q05 | qualitative_noisy | Reddit 2.pdf | Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf; Reddit 2.pdf |
| Q06 | historical_analysis | Reddit 3.pdf | Reddit 3.pdf; Reddit 3.pdf; Reddit 3.pdf; Reddit 3.pdf; Reddit 3.pdf |
| Q07 | historical_qa | Reddit 4.pdf | Reddit 4.pdf; Reddit 4.pdf; Reddit 4.pdf; Reddit 4.pdf; Reddit 4.pdf |
| Q08 | quantitative_excel | regular NBA.xlsx (Feuille: Données NBA) | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Dictionnaire des données); Reddit 3.pdf |
| Q09 | quantitative_excel | regular NBA.xlsx (Feuille: Données NBA) | regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse Vide) |
| Q10 | quantitative_limit | regular NBA.xlsx (Feuille: Données NBA); regular NBA.xlsx (Feuille: Dictionnaire des données) | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Dictionnaire des données) |

## Lecture rapide

- Les cas qualitatifs testent la capacite du RAG texte a retrouver et synthetiser les PDF Reddit.
- Les cas quantitatifs testent les limites de l'Excel indexe comme texte.
- Le cas Q10 doit rester prudent, car les donnees actuelles ne contiennent pas de split sur les cinq derniers matchs.
