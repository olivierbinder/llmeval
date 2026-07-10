# Evaluation RAGAS - nba_rag_eval_baseline v3

**Experience** : `pydantic_ai_constrained_rag`

## Vue d'ensemble

- Cas evalues : **10**
- Scores RAGAS calcules : **39/40**
- Scores manquants : **1**

| Metrique | Score moyen |
|---|---:|
| `faithfulness` | 0.900 |
| `answer_relevancy` | 0.517 |
| `context_precision` | 0.639 |
| `context_recall` | 0.535 |

## Scores par categorie

| Categorie | Faithfulness | Answer relevancy | Context precision | Context recall | Cas |
|---|---:|---:|---:|---:|---:|
| historical_analysis | 1.000 | 0.898 | 0.887 | 0.500 | 1 |
| historical_qa | 1.000 | 0.935 | 0.804 | 1.000 | 1 |
| qualitative_comparison | 1.000 | 0.887 | 0.500 | 0.600 | 1 |
| qualitative_complex | 1.000 | 0.803 | 1.000 | 0.000 | 1 |
| qualitative_noisy | 1.000 | 0.000 | n/a | 1.000 | 1 |
| qualitative_simple | 0.875 | 0.826 | 0.875 | 0.750 | 2 |
| quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | 2 |
| quantitative_limit | 0.250 | 0.000 | 0.806 | 0.750 | 1 |

## Synthese des cas

| Cas | Categorie | Faithfulness | Relevancy | Precision | Recall | Confiance | Contexte insuffisant |
|---|---|---:|---:|---:|---:|---|---:|
| Q01 | qualitative_simple | 0.750 | 0.843 | 0.750 | 0.500 | medium | non |
| Q02 | qualitative_simple | 1.000 | 0.808 | 1.000 | 1.000 | high | non |
| Q03 | qualitative_comparison | 1.000 | 0.887 | 0.500 | 0.600 | high | non |
| Q04 | qualitative_complex | 1.000 | 0.803 | 1.000 | 0.000 | high | non |
| Q05 | qualitative_noisy | 1.000 | 0.000 | n/a | 1.000 | medium | non |
| Q06 | historical_analysis | 1.000 | 0.898 | 0.887 | 0.500 | medium | non |
| Q07 | historical_qa | 1.000 | 0.935 | 0.804 | 1.000 | high | non |
| Q08 | quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | low | oui |
| Q09 | quantitative_excel | 1.000 | 0.000 | 0.000 | 0.000 | low | oui |
| Q10 | quantitative_limit | 0.250 | 0.000 | 0.806 | 0.750 | low | oui |

## Detail par cas

### Q01 — qualitative_simple

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | medium |
| Contexte insuffisant | non |
| Faithfulness | 0.750 |
| Answer relevancy | 0.843 |
| Context precision | 0.750 |
| Context recall | 0.500 |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf; Reddit 2.pdf |
| Scores retrieval | 82.94; 81.37; 81.35; 81.25; 79.98 |

**Question**

> Pourquoi le Magic d'Orlando est-il présenté comme une équipe prometteuse dans la discussion playoff ?

**Reponse attendue YAML**

> La discussion présente Orlando comme une jeune équipe prometteuse parce que Paolo Banchero et Franz Wagner sont décrits comme un duo d'ailiers solide, capable de scorer, de défendre et de poser des problèmes au champion en titre malgré un spacing faible et des absences importantes. La principale limite mentionnée est qu'Orlando a encore besoin de meilleurs shooteurs et d'un vrai meneur.

**Reponse du LLM**

> Le Magic d'Orlando est présenté comme une équipe prometteuse en raison de la croissance de ses jeunes joueurs comme Paolo et les Wagner, ainsi que de la performance de Franz Wagner et de la gestion du jeu par Dennis Schroeder. Malgré des blessures et un manque de tireurs à trois points fiables, leur potentiel et leur résilience sont soulignés, notamment s'ils améliorent leur adresse à longue distance.

### Q02 — qualitative_simple

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | 1.000 |
| Answer relevancy | 0.808 |
| Context precision | 1.000 |
| Context recall | 1.000 |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf |
| Scores retrieval | 82.31; 81.20; 79.75; 79.31; 79.30 |

**Question**

> D'après la discussion Reddit, qu'est-ce qui a changé dans l'impact de Julius Randle en playoffs ?

**Reponse attendue YAML**

> Les commentaires expliquent que Randle paraît beaucoup plus efficace que ne le suggérait son ancienne réputation en playoffs. Ils citent son jeu physique en attaque, ses meilleures lectures face aux prises à deux, son engagement défensif et une forte progression à trois points, avec une mention d'un tir à 45 % de loin.

**Reponse du LLM**

> D'après les discussions, Julius Randle a changé son approche en playoffs : il a abandonné le style "beyblade" (mouvements de spin excessifs) pour adopter un jeu plus physique et efficace en isolation, tout en améliorant son engagement défensif et sa capacité à lire les doubles équipes.

### Q03 — qualitative_comparison

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | 1.000 |
| Answer relevancy | 0.887 |
| Context precision | 0.500 |
| Context recall | 0.600 |
| Sources attendues | Reddit 1.pdf |
| Sources utilisees par le LLM | Reddit 1.pdf |
| Sources retrouvees par FAISS | Reddit 1.pdf |
| Scores retrieval | 85.78; 84.44; 84.33; 83.95; 83.91 |

**Question**

> Quelles équipes sont régulièrement décrites comme impressionnantes en playoffs, et pourquoi ?

**Reponse attendue YAML**

> Le fil mentionne notamment le Magic, les Pacers, les Timberwolves et les Pistons. Orlando est valorisé pour le duo Paolo-Franz qui a gêné Boston malgré des limites offensives. Indiana est cité pour une attaque capable de poser problème à n'importe qui et pour une domination plus nette que l'année précédente. Minnesota est loué pour son plafond élevé, son équilibre attaque/défense, la progression d'Anthony Edwards et une attaque plus collective. Detroit est apprécié pour le niveau et le leadership de Cade Cunningham, même si l'équipe semble encore avoir besoin d'un créateur ou d'un shooteur supplémentaire.

**Reponse du LLM**

> Les équipes régulièrement décrites comme impressionnantes en playoffs sont les Timberwolves, grâce à leur collectif fort et à des joueurs comme Edwards qui ont réalisé un grand bond en avant. Les Celtics et les Cavaliers sont également mentionnés pour leur performance conforme aux attentes. Les Warriors sont salués pour leur expérience en playoffs et leur capacité à surmonter les défis, malgré des difficultés offensives face à des défenses physiques.

### Q04 — qualitative_complex

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | 1.000 |
| Answer relevancy | 0.803 |
| Context precision | 1.000 |
| Context recall | 0.000 |
| Sources attendues | Reddit 2.pdf |
| Sources utilisees par le LLM | Reddit 2.pdf |
| Sources retrouvees par FAISS | Reddit 2.pdf |
| Scores retrieval | 85.08; 84.74; 84.61; 83.94; 83.48 |

**Question**

> Pourquoi certains fans estiment-ils qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse ?

**Reponse attendue YAML**

> La discussion soutient que cette affiche réunirait de très bonnes équipes de basket et que le cadrage négatif vient surtout des médias NBA et des habitudes du public occasionnel. Les fans se concentreraient souvent sur les highlights, les superstars, les gros marchés et les noms familiers plutôt que sur la qualité collective. Un commentaire rappelle que le Thunder est statistiquement excellent et que les Pacers enchaînent deux finales de conférence, mais que la parité et les petits marchés rendent l'intérêt plus difficile à construire pour les spectateurs occasionnels.

**Reponse du LLM**

> Certains fans estiment qu'une finale Thunder-Pacers ne devrait pas être considérée comme ennuyeuse car les deux équipes sont complètes, possèdent chacune une superstar capable de prendre le jeu en main, et offrent un style de jeu dynamique avec des remontées spectaculaires. De plus, leur affrontement en playoffs serait perçu comme historique en raison de la domination statistique des Thunder et du parcours surprenant des Pacers.

### Q05 — qualitative_noisy

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | medium |
| Contexte insuffisant | non |
| Faithfulness | 1.000 |
| Answer relevancy | 0.000 |
| Context precision | n/a |
| Context recall | 1.000 |
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
| Faithfulness | 1.000 |
| Answer relevancy | 0.898 |
| Context precision | 0.887 |
| Context recall | 0.500 |
| Sources attendues | Reddit 3.pdf |
| Sources utilisees par le LLM | Reddit 3.pdf |
| Sources retrouvees par FAISS | Reddit 3.pdf |
| Scores retrieval | 88.34; 88.28; 88.02; 87.64; 87.50 |

**Question**

> Quel est l'argument principal pour présenter Reggie Miller comme une première option historiquement efficace en playoffs ?

**Reponse attendue YAML**

> L'argument principal est que Reggie Miller arrive en tête d'une comparaison des premières options offensives en efficacité au scoring en playoffs, ajustée au contexte de son époque. Le post affirme que son écart d'efficacité avec des joueurs comme Stephen Curry est important, et que même en se limitant à son prime de 1991 à 2002, il marque environ 24 points par match sur plus de 100 matchs de playoffs avec un relative true shooting de 115. La discussion nuance aussi ce point en rappelant que son volume de tirs est inférieur à celui de nombreux autres grands scoreurs.

**Reponse du LLM**

> L'argument principal avancé est que Reggie Miller a mené son équipe en playoffs avec une grande efficacité, notamment en termes de réussite et d'impact, malgré une utilisation (USG%) modérée. Certains soulignent qu'il a remporté 14 séries éliminatoires avec les Pacers, souvent en tant que meilleur marqueur ou contributeur clé, et qu'il a augmenté significativement sa production lors des matchs décisifs.

### Q07 — historical_qa

| Champ | Valeur |
|---|---|
| Source type | reddit |
| Confiance LLM | high |
| Contexte insuffisant | non |
| Faithfulness | 1.000 |
| Answer relevancy | 0.935 |
| Context precision | 0.804 |
| Context recall | 1.000 |
| Sources attendues | Reddit 4.pdf |
| Sources utilisees par le LLM | Reddit 4.pdf |
| Sources retrouvees par FAISS | Reddit 4.pdf |
| Scores retrieval | 85.70; 84.84; 84.76; 84.57; 84.22 |

**Question**

> Quelle équipe NBA n'a pas eu l'avantage du terrain avant les Finales, puis l'a eu en Finales ?

**Reponse attendue YAML**

> La réponse attendue d'après le fil est qu'il n'existe probablement pas de telle équipe dans la NBA moderne. Un commentaire indique que six équipes classées plus bas qu'une quatrième place ont atteint les Finales, mais qu'aucune n'y avait l'avantage du terrain. Le Heat 2023 est mentionné comme quasi-exemple, mais Denver avait l'avantage du terrain dans ces Finales, donc Miami ne répond pas à la question.

**Reponse du LLM**

> Les Rockets de Houston en 1995 sont l'équipe NBA qui n'a pas eu l'avantage du terrain avant les Finales, puis l'a eu en Finales après avoir remporté le titre.

### Q08 — quantitative_excel

| Champ | Valeur |
|---|---|
| Source type | excel |
| Confiance LLM | low |
| Contexte insuffisant | oui |
| Faithfulness | 1.000 |
| Answer relevancy | 0.000 |
| Context precision | 0.000 |
| Context recall | 0.000 |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA) |
| Sources utilisees par le LLM | regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Analyse); Reddit 3.pdf |
| Scores retrieval | 85.46; 84.87; 84.74; 83.49; 81.62 |

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
| Faithfulness | 1.000 |
| Answer relevancy | 0.000 |
| Context precision | 0.000 |
| Context recall | 0.000 |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA) |
| Sources utilisees par le LLM | regular NBA.xlsx (Feuille: Analyse) |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide); regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Scores retrieval | 82.90; 82.83; 82.43; 80.64; 80.42 |

**Question**

> Quel joueur a le plus grand total de rebonds dans la table Excel des joueurs ?

**Reponse attendue YAML**

> Ivica Zubac possède le plus grand total de rebonds dans la table Excel des joueurs, avec 1008 rebonds pour les Los Angeles Clippers. Les joueurs suivants dans ce classement incluent Domantas Sabonis avec 973 rebonds, Karl-Anthony Towns avec 922 et Nikola Jokic avec 889.

**Reponse du LLM**

> Les contextes fournis ne permettent pas de déterminer quel joueur a le plus grand total de rebonds, car la colonne dédiée aux rebonds totaux n'est pas disponible dans les données partagées.

### Q10 — quantitative_limit

| Champ | Valeur |
|---|---|
| Source type | excel |
| Confiance LLM | low |
| Contexte insuffisant | oui |
| Faithfulness | 0.250 |
| Answer relevancy | 0.000 |
| Context precision | 0.806 |
| Context recall | 0.750 |
| Sources attendues | regular NBA.xlsx (Feuille: Données NBA); regular NBA.xlsx (Feuille: Dictionnaire des données) |
| Sources utilisees par le LLM | n/a |
| Sources retrouvees par FAISS | regular NBA.xlsx (Feuille: Dictionnaire des données); regular NBA.xlsx (Feuille: Analyse); regular NBA.xlsx (Feuille: Analyse Vide) |
| Scores retrieval | 82.53; 82.06; 81.52; 81.36; 81.00 |

**Question**

> Quel joueur a le meilleur pourcentage à trois points sur les cinq derniers matchs ?

**Reponse attendue YAML**

> Les sources actuellement indexées ne fournissent pas de lignes match par match ni de découpage sur les cinq derniers matchs. Le prototype ne doit donc pas inventer une réponse exacte sur cette période. Le classeur Excel contient des agrégats de saison comme GP, 3PA et 3P%, qui permettent de répondre à des questions au niveau saison, mais pas d'établir de façon fiable un classement sur les cinq derniers matchs. Ce cas devrait s'améliorer seulement après l'ajout d'une base structurée avec des statistiques par match.

**Reponse du LLM**

> Les contextes fournis ne contiennent pas de données sur les cinq derniers matchs ou de pourcentage à trois points pour cette période. Seuls les pourcentages de réussite à trois points en moyenne par match sont disponibles, mais pas pour une période spécifique.


## Lecture rapide

- Les reponses courtes viennent de la sortie structuree Pydantic AI.
- `used_sources`, `confidence` et `insufficient_context` sont produits par le LLM via le schema de sortie.
- `retrieved_sources` correspond aux chunks recuperes par FAISS, pas forcement aux sources vraiment utilisees par le LLM.
- Les cas Excel restent limites par l'indexation texte du classeur : les calculs fiables devront passer par une base structuree ou un outil SQL.
- Les scores `n/a` indiquent generalement une metrique RAGAS non calculee, souvent a cause d'un timeout, d'un rate limit ou d'une sortie juge invalide.
