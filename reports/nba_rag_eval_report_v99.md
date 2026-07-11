# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_baseline`
- **Version** : `v99`
- **Experience** : `Test Erreur`
- **Duree d'execution** : `53s`
- **Cas evalues** : `1`
- **Scores RAGAS calcules** : `4/4`

## Scores moyens

| Metrique | Score moyen |
|---|---:|
| `faithfulness` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| `answer_relevancy` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98cf7e; color:#000000; text-align:center;">0.807</span> |
| `context_precision` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| `context_recall` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |

## Scores par categorie

| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |
|---|---:|---:|---:|---:|---:|
| qualitative_complex | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98cf7e; color:#000000; text-align:center;">0.807</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | 1 |

## Synthese des cas

| Cas | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contexte insuffisant |
|---|---|---:|---:|---:|---:|---|---:|
| Q04 | qualitative_complex | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98cf7e; color:#000000; text-align:center;">0.807</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | high | non |

## Detail par cas

### Q04 — qualitative_complex

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98cf7e; color:#000000; text-align:center;">0.807</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Sources attendues | Reddit 2.pdf |
| Sources utilisees par le LLM | Reddit 2.pdf |
| Sources retrouvees par FAISS | Reddit 2.pdf |
| Scores retrieval | 85.07; 84.74; 84.59; 83.96; 83.47 |

**Question**

> Pourquoi certains fans estiment-ils qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse ?

**Reponse attendue YAML**

> La discussion soutient que cette affiche réunirait de très bonnes équipes de basket et que le cadrage négatif vient surtout des médias NBA et des habitudes du public occasionnel. Les fans se concentreraient souvent sur les highlights, les superstars, les gros marchés et les noms familiers plutôt que sur la qualité collective. Un commentaire rappelle que le Thunder est statistiquement excellent et que les Pacers enchaînent deux finales de conférence, mais que la parité et les petits marchés rendent l'intérêt plus difficile à construire pour les spectateurs occasionnels.

**Reponse du LLM**

> Certains fans estiment qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse car les deux équipes sont complètes, possèdent chacune une superstar capable de prendre le jeu en main, et offrent un style de jeu différent : OKC avec un rythme élevé et une défense solide, tandis que l'Indiana mise sur un jeu collectif et des remontées spectaculaires.

