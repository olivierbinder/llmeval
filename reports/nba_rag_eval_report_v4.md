# Evaluation RAGAS NBA Analyst AI

- **Jeu de questions** : `nba_rag_eval_baseline`
- **Version** : `v4`
- **Experience** : `pydantic_ai_constrained_rag`
- **Duree d'execution** : `9min 5s`
- **Cas evalues** : `10`
- **Scores RAGAS calcules** : `39/40`

## Scores moyens

| Metrique | Score moyen |
|---|---:|
| `faithfulness` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#99d07f; color:#000000; text-align:center;">0.800</span> |
| `answer_relevancy` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8d980; color:#000000; text-align:center;">0.429</span> |
| `context_precision` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#cfe282; color:#000000; text-align:center;">0.605</span> |
| `context_recall` | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#c6df82; color:#000000; text-align:center;">0.635</span> |

## Scores par categorie

| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |
|---|---:|---:|---:|---:|---:|
| historical_analysis | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7dc77d; color:#ffffff; text-align:center;">0.903</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#82c87d; color:#ffffff; text-align:center;">0.887</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#ebeb84; color:#000000; text-align:center;">0.500</span> | 1 |
| historical_qa | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#99d07f; color:#000000; text-align:center;">0.802</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98d07f; color:#000000; text-align:center;">0.804</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | 1 |
| qualitative_comparison | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7fc77d; color:#ffffff; text-align:center;">0.896</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8aa77; color:#ffffff; text-align:center;">0.250</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#d0e282; color:#000000; text-align:center;">0.600</span> | 1 |
| qualitative_complex | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#eeeeee; color:#555555; text-align:center;">n/a</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | 1 |
| qualitative_noisy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | 1 |
| qualitative_simple | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#90cd7e; color:#000000; text-align:center;">0.833</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#8dcc7e; color:#000000; text-align:center;">0.845</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#85c97d; color:#ffffff; text-align:center;">0.875</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d480; color:#000000; text-align:center;">0.750</span> | 2 |
| quantitative_excel | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | 2 |
| quantitative_limit | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8c07c; color:#ffffff; text-align:center;">0.333</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d580; color:#000000; text-align:center;">0.750</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d480; color:#000000; text-align:center;">0.750</span> | 1 |

## Synthese des cas

| Cas | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contexte insuffisant |
|---|---|---:|---:|---:|---:|---|---:|
| Q01 | qualitative_simple | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#82c87d; color:#ffffff; text-align:center;">0.886</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d580; color:#000000; text-align:center;">0.750</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#ebeb84; color:#000000; text-align:center;">0.500</span> | medium | non |
| Q02 | qualitative_simple | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98d07f; color:#000000; text-align:center;">0.805</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | high | non |
| Q03 | qualitative_comparison | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7fc77d; color:#ffffff; text-align:center;">0.896</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8aa77; color:#ffffff; text-align:center;">0.250</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#d0e282; color:#000000; text-align:center;">0.600</span> | high | non |
| Q04 | qualitative_complex | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#eeeeee; color:#555555; text-align:center;">n/a</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | high | non |
| Q05 | qualitative_noisy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | medium | non |
| Q06 | historical_analysis | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7dc77d; color:#ffffff; text-align:center;">0.903</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#82c87d; color:#ffffff; text-align:center;">0.887</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#ebeb84; color:#000000; text-align:center;">0.500</span> | medium | non |
| Q07 | historical_qa | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#99d07f; color:#000000; text-align:center;">0.802</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98d07f; color:#000000; text-align:center;">0.804</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | high | non |
| Q08 | quantitative_excel | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | low | oui |
| Q09 | quantitative_excel | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8c07c; color:#ffffff; text-align:center;">0.333</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | low | oui |
| Q10 | quantitative_limit | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8c07c; color:#ffffff; text-align:center;">0.333</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d580; color:#000000; text-align:center;">0.750</span> | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d480; color:#000000; text-align:center;">0.750</span> | low | oui |

## Detail par cas

### Q01 — qualitative_simple

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | medium |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#82c87d; color:#ffffff; text-align:center;">0.886</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d580; color:#000000; text-align:center;">0.750</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#ebeb84; color:#000000; text-align:center;">0.500</span> |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf; Reddit 2.pdf |
| Scores retrieval | 82.94; 81.37; 81.35; 81.25; 79.98 |

**Question**

> Pourquoi le Magic d'Orlando est-il présenté comme une équipe prometteuse dans la discussion playoff ?

**Reponse attendue YAML**

> La discussion présente Orlando comme une jeune équipe prometteuse parce que Paolo Banchero et Franz Wagner sont décrits comme un duo d'ailiers solide, capable de scorer, de défendre et de poser des problèmes au champion en titre malgré un spacing faible et des absences importantes. La principale limite mentionnée est qu'Orlando a encore besoin de meilleurs shooteurs et d'un vrai meneur.

**Reponse du LLM**

> Le Magic d'Orlando est présenté comme une équipe prometteuse en raison de la croissance de ses jeunes joueurs comme Paolo et les Wagner, ainsi que de la performance de Franz Wagner et de la gestion du jeu par Dennis Schroeder. Leur capacité à rivaliser malgré des blessures et leur potentiel offensif futur sont également soulignés.

### Q02 — qualitative_simple

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98d07f; color:#000000; text-align:center;">0.805</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf |
| Scores retrieval | 82.31; 81.20; 79.75; 79.31; 79.30 |

**Question**

> D'après la discussion Reddit, qu'est-ce qui a changé dans l'impact de Julius Randle en playoffs ?

**Reponse attendue YAML**

> Les commentaires expliquent que Randle paraît beaucoup plus efficace que ne le suggérait son ancienne réputation en playoffs. Ils citent son jeu physique en attaque, ses meilleures lectures face aux prises à deux, son engagement défensif et une forte progression à trois points, avec une mention d'un tir à 45 % de loin.

**Reponse du LLM**

> D'après les discussions, Julius Randle a changé son approche en playoffs : il a abandonné le style "beyblade" (mouvements de spin excessifs) pour adopter un jeu plus physique et efficace en isolation, tout en améliorant son engagement défensif et sa capacité à lire les doubles marquages.

### Q03 — qualitative_comparison

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7fc77d; color:#ffffff; text-align:center;">0.896</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8aa77; color:#ffffff; text-align:center;">0.250</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#d0e282; color:#000000; text-align:center;">0.600</span> |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf |
| Scores retrieval | 85.78; 84.44; 84.33; 83.95; 83.91 |

**Question**

> Quelles équipes sont régulièrement décrites comme impressionnantes en playoffs, et pourquoi ?

**Reponse attendue YAML**

> Le fil mentionne notamment le Magic, les Pacers, les Timberwolves et les Pistons. Orlando est valorisé pour le duo Paolo-Franz qui a gêné Boston malgré des limites offensives. Indiana est cité pour une attaque capable de poser problème à n'importe qui et pour une domination plus nette que l'année précédente. Minnesota est loué pour son plafond élevé, son équilibre attaque/défense, la progression d'Anthony Edwards et une attaque plus collective. Detroit est apprécié pour le niveau et le leadership de Cade Cunningham, même si l'équipe semble encore avoir besoin d'un créateur ou d'un shooteur supplémentaire.

**Reponse du LLM**

> Les équipes régulièrement décrites comme impressionnantes en playoffs sont les Timberwolves, grâce à leur collectif fort et à des joueurs comme Edwards qui ont réalisé un bond qualitatif. Les Celtics et les Cavaliers sont également mentionnés pour leur performance conforme aux attentes. Les Warriors sont salués pour leur expérience en playoffs et leur capacité à surmonter les défis.

### Q04 — qualitative_complex

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#eeeeee; color:#555555; text-align:center;">n/a</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Sources attendues | Reddit 2.pdf |
| Sources utilisees par le LLM | Reddit 2.pdf |
| Sources retrouvees par FAISS | Reddit 2.pdf |
| Scores retrieval | 85.09; 84.77; 84.63; 83.96; 83.49 |

**Question**

> Pourquoi certains fans estiment-ils qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse ?

**Reponse attendue YAML**

> La discussion soutient que cette affiche réunirait de très bonnes équipes de basket et que le cadrage négatif vient surtout des médias NBA et des habitudes du public occasionnel. Les fans se concentreraient souvent sur les highlights, les superstars, les gros marchés et les noms familiers plutôt que sur la qualité collective. Un commentaire rappelle que le Thunder est statistiquement excellent et que les Pacers enchaînent deux finales de conférence, mais que la parité et les petits marchés rendent l'intérêt plus difficile à construire pour les spectateurs occasionnels.

**Reponse du LLM**

> Certains fans estiment qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse car les deux équipes sont complètes, possèdent chacune une superstar capable de prendre le jeu en main, et offrent un style de jeu dynamique. Les Pacers, malgré un manque de visibilité médiatique nationale, ont démontré des capacités de comeback et une bonne circulation de balle, tandis que les Thunder jouent à un rythme élevé et avec une défense solide.

### Q05 — qualitative_noisy

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | medium |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Sources attendues | Reddit 2.pdf |
| Sources utilisees par le LLM | Reddit 2.pdf |
| Sources retrouvees par FAISS | Reddit 2.pdf |
| Scores retrieval | 84.03; 82.50; 82.42; 81.97; 81.86 |

**Question**

> Franchement, une finale Pacers-Thunder serait vraiment ennuyeuse ou les fans dramatisent ?

**Reponse attendue YAML**

> Le fil suggère qu'une telle finale ne serait pas forcément ennuyeuse. Plusieurs commentaires s'attendent à une bonne série Pacers-Thunder, potentiellement toxique en ligne, et imaginent même des matchs serrés avec Shai Gilgeous-Alexander et Tyrese Haliburton au premier plan. La négativité semble relever davantage du discours des fans et de la perception médiatique que d'une preuve que le basket proposé serait mauvais.

**Reponse du LLM**

> Les avis sont partagés. Certains fans estiment que cette finale serait ennuyeuse en raison du style de jeu d'OKC, jugé trop défensif et centré sur Shai Gilgeous-Alexander, tandis que d'autres soulignent l'efficacité et l'équilibre des deux équipes, ainsi que leur capacité à dicter le rythme des matchs. Les débats portent aussi sur le manque de visibilité des Pacers avant les playoffs, ce qui pourrait influencer la perception de leur jeu.

### Q06 — historical_analysis

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | medium |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#7dc77d; color:#ffffff; text-align:center;">0.903</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#82c87d; color:#ffffff; text-align:center;">0.887</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#ebeb84; color:#000000; text-align:center;">0.500</span> |
| Sources attendues | Reddit 3.pdf |
| Sources utilisees par le LLM | Reddit 3.pdf |
| Sources retrouvees par FAISS | Reddit 3.pdf |
| Scores retrieval | 88.32; 88.26; 88.00; 87.60; 87.48 |

**Question**

> Quel est l'argument principal pour présenter Reggie Miller comme une première option historiquement efficace en playoffs ?

**Reponse attendue YAML**

> L'argument principal est que Reggie Miller arrive en tête d'une comparaison des premières options offensives en efficacité au scoring en playoffs, ajustée au contexte de son époque. Le post affirme que son écart d'efficacité avec des joueurs comme Stephen Curry est important, et que même en se limitant à son prime de 1991 à 2002, il marque environ 24 points par match sur plus de 100 matchs de playoffs avec un relative true shooting de 115. La discussion nuance aussi ce point en rappelant que son volume de tirs est inférieur à celui de nombreux autres grands scoreurs.

**Reponse du LLM**

> L'argument principal avancé est que Reggie Miller a mené son équipe en playoffs avec une grande efficacité, notamment en termes de réussite et d'impact, malgré une utilisation (USG%) modérée. Certains soulignent qu'il a été la première option offensive des Pacers lors de 14 séries éliminatoires remportées, avec des performances accrues en playoffs par rapport à la saison régulière.

### Q07 — historical_qa

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#bedc81; color:#000000; text-align:center;">0.667</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#99d07f; color:#000000; text-align:center;">0.802</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#98d07f; color:#000000; text-align:center;">0.804</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Sources attendues | Reddit 4.pdf |
| Sources utilisees par le LLM | Reddit 4.pdf |
| Sources retrouvees par FAISS | Reddit 4.pdf |
| Scores retrieval | 85.73; 84.87; 84.78; 84.60; 84.25 |

**Question**

> Quelle équipe NBA n'a pas eu l'avantage du terrain avant les Finales, puis l'a eu en Finales ?

**Reponse attendue YAML**

> La réponse attendue d'après le fil est qu'il n'existe probablement pas de telle équipe dans la NBA moderne. Un commentaire indique que six équipes classées plus bas qu'une quatrième place ont atteint les Finales, mais qu'aucune n'y avait l'avantage du terrain. Le Heat 2023 est mentionné comme quasi-exemple, mais Denver avait l'avantage du terrain dans ces Finales, donc Miami ne répond pas à la question.

**Reponse du LLM**

> Les Rockets de Houston en 1995 sont l'équipe la plus citée pour avoir remporté le titre sans avoir eu l'avantage du terrain avant les Finales, puis l'ayant eu en Finales.

### Q08 — quantitative_excel

| Champ | Valeur |
|---|---|
| Source type | excel |
| Confiance LLM | low |
| Contexte insuffisant | oui |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#63be7b; color:#ffffff; text-align:center;">1.000</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA) |
| Sources utilisees par le LLM | regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Analyse); Reddit 3.pdf |
| Scores retrieval | 85.48; 84.88; 84.74; 83.52; 81.63 |

**Question**

> Parmi les joueurs avec au moins 300 tentatives à trois points, qui a le meilleur pourcentage à trois points dans les données Excel ?

**Reponse attendue YAML**

> Zach LaVine possède le meilleur pourcentage à trois points parmi les joueurs avec au moins 300 tentatives dans la table Excel : 44,6 % sur 533 tentatives avec Sacramento. Les autres shooteurs à gros volume visibles en haut du classement incluent Taurean Prince à 43,9 %, Harrison Barnes et Keon Ellis à 43,3 %, puis Kevin Durant à 43,0 %.

**Reponse du LLM**

> Les données fournies ne permettent pas d'identifier les joueurs avec au moins 300 tentatives à trois points ni leur pourcentage de réussite à 3 points.

### Q09 — quantitative_excel

| Champ | Valeur |
|---|---|
| Source type | excel |
| Confiance LLM | low |
| Contexte insuffisant | oui |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8c07c; color:#ffffff; text-align:center;">0.333</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA) |
| Sources utilisees par le LLM | n/a |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Scores retrieval | 82.90; 82.83; 82.43; 80.64; 80.42 |

**Question**

> Quel joueur a le plus grand total de rebonds dans la table Excel des joueurs ?

**Reponse attendue YAML**

> Ivica Zubac possède le plus grand total de rebonds dans la table Excel des joueurs, avec 1008 rebonds pour les Los Angeles Clippers. Les joueurs suivants dans ce classement incluent Domantas Sabonis avec 973 rebonds, Karl-Anthony Towns avec 922 et Nikola Jokic avec 889.

**Reponse du LLM**

> Les contextes fournis ne permettent pas de répondre précisément à cette question, car la colonne "Rebonds offensifs" ne représente pas le total de rebonds mais uniquement les rebonds offensifs.

### Q10 — quantitative_limit

| Champ | Valeur |
|---|---|
| Source type | excel |
| Confiance LLM | low |
| Contexte insuffisant | oui |
| Faithfulness | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8c07c; color:#ffffff; text-align:center;">0.333</span> |
| Answer relevancy | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#f8696b; color:#ffffff; text-align:center;">0.000</span> |
| Context precision | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d580; color:#000000; text-align:center;">0.750</span> |
| Context recall | <span style="display:inline-block; min-width:52px; padding:2px 6px; border-radius:4px; background-color:#a7d480; color:#000000; text-align:center;">0.750</span> |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA); regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Sources utilisees par le LLM | n/a |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide) |
| Scores retrieval | 82.53; 82.06; 81.52; 81.36; 81.00 |

**Question**

> Quel joueur a le meilleur pourcentage à trois points sur les cinq derniers matchs ?

**Reponse attendue YAML**

> Les sources actuellement indexées ne fournissent pas de lignes match par match ni de découpage sur les cinq derniers matchs. Le prototype ne doit donc pas inventer une réponse exacte sur cette période. Le classeur Excel contient des agrégats de saison comme GP, 3PA et 3P%, qui permettent de répondre à des questions au niveau saison, mais pas d'établir de façon fiable un classement sur les cinq derniers matchs. Ce cas devrait s'améliorer seulement après l'ajout d'une base structurée avec des statistiques par match.

**Reponse du LLM**

> Les contextes fournis ne contiennent pas de données sur les cinq derniers matchs ou de pourcentage à trois points pour cette période. Seuls les pourcentages de réussite à 3 points en moyenne par match sont disponibles.

