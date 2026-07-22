# Résultats

<div class="lead-callout">
Deux expériences sont comparées : un RAG uniquement FAISS et un pipeline hybride FAISS + SQL.
</div>

Sources :

- `reports/nba_rag_eval_report_v0.md` : expérience `faiss only`
- `reports/nba_rag_eval_report_v1.md` : expérience `with_sql_strategy`

## Vue d'ensemble

| Expérience | Stratégie | Durée run | Faithfulness | Relevancy | Precision | Recall |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `v0` | FAISS only | `9min 9s` | 0.817 | 0.611 | 0.642 | 0.542 |
| `v1` | Hybride SQL | `8min 14s` | 0.875 | 0.825 | 0.762 | 0.742 |

Lecture simple :

- L'hybride améliore les 4 scores RAGAS moyens.
- Le gain vient surtout des questions quantitatives Excel traitées réellement par SQL.
- Le run hybride est plus coûteux pour générer les réponses, mais plus rapide au total sur cette exécution.

## Performance

| Indicateur | FAISS only `v0` | Hybride SQL `v1` |
| --- | ---: | ---: |
| Appels LLM réponse agent | 10 | 24 |
| Temps API réponse agent | `11.19s` | `21.24s` |
| Tokens entrée réponse agent | 25 879 | 45 896 |
| Tokens sortie réponse agent | 948 | 1 668 |
| Temps total RAGAS | `529.57s` | `469.85s` |
| Appels juge RAGAS | 110 | 102 |
| Appels embeddings RAGAS | 20 | 20 |

Le chemin SQL demande plus d'appels pendant la génération : l'agent inspecte le schéma, exécute une requête, puis reformule la réponse. En contrepartie, les contextes donnés à RAGAS pour les cas SQL sont plus courts et plus ciblés.

## Scores sur les questions SQL

Cette comparaison ne prend en compte que `Q08` et `Q09`, car `Q10` bascule en fallback FAISS.

| Expérience | Faithfulness | Relevancy | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| FAISS only `v0` | 0.500 | 0.000 | 0.100 | 0.000 |
| Hybride SQL `v1` | 1.000 | 0.956 | 1.000 | 1.000 |

## Réponses SQL

| Cas | Question | Réponse FAISS only `v0` | Réponse hybride SQL `v1` |
| --- | --- | --- | --- |
| `Q08` | Parmi les joueurs avec au moins 300 tirs à trois points tentés, qui a le meilleur pourcentage ? | Les contextes ne permettent pas de répondre précisément à cette question. | Zach LaVine détient le meilleur pourcentage à trois points (44,6 %) parmi les joueurs ayant tenté au moins 300 tirs à trois points, avec 237 paniers réussis sur 533 tentés. |
| `Q09` | Quel joueur possède le plus grand total de rebonds dans la table des joueurs ? | Les contextes ne permettent pas de répondre précisément à cette question. | Ivica Zubac possède le plus grand total de rebonds avec 1008. |

## Cas limite avec fallback

`Q10` demande le meilleur pourcentage à trois points sur les cinq derniers matchs. Cette donnée n'est pas disponible dans la base structurée, qui contient des agrégats de saison.

| Cas | Question | Réponse FAISS only `v0` | Réponse hybride `v1` |
| --- | --- | --- | --- |
| `Q10` | Qui a le meilleur pourcentage à trois points sur ses cinq derniers matchs ? | Les contextes ne permettent pas de déterminer qui a le meilleur pourcentage à trois points sur les cinq derniers matchs. | Les contextes fournis ne contiennent pas de données sur les cinq derniers matchs ou de pourcentage à trois points par période récente. |

## Conclusion

| Point comparé | Résultat |
| --- | --- |
| Questions qualitatives | FAISS reste adapté. |
| Questions quantitatives disponibles en base | SQL répond beaucoup mieux sur `Q08` et `Q09`. |
| Questions quantitatives absentes de la base | Le système doit refuser ou fallback proprement. |
| Coût génération | L'hybride coûte plus d'appels et de tokens. |
| Évaluation RAGAS | L'hybride obtient de meilleurs scores sur ce jeu de 10 cas. |

Le choix final dépend donc du besoin : FAISS seul est plus simple et moins coûteux, mais l'hybride est nettement plus fiable dès qu'une question demande un calcul exact sur les données Excel.
