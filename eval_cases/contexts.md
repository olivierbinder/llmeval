## 10 questions d'evaluation

Cette section indique ou retrouver l'information source qui permet de repondre aux cas `Q01` a `Q10`.
Pour les PDF, les positions sont donnees en pages PDF. Les pages proviennent des marqueurs OCR presents dans les documents (`1/15`, `2/15`, etc.) et peuvent couvrir deux pages quand un chunk FAISS chevauche une coupure.
Pour Excel, les positions sont donnees avec la feuille, la table SQLite et les colonnes utilisees.

### Q01 - Julius Randle plus convaincant en playoffs

- Question : Qu'est-ce qui rend Julius Randle plus convaincant dans ces playoffs selon les commentaires ?
- Source attendue : `inputs/Reddit 1.pdf`.
- Emplacement dans le PDF :
  - `Reddit 1.pdf`, pages `1-2` : passages sur Randle, son bully ball, son impact offensif, ses lectures face aux prises a deux et son engagement defensif.
  - `Reddit 1.pdf`, pages `2-3` : passages sur sa reputation en playoffs et le contexte des anciennes critiques.
  - `Reddit 1.pdf`, pages `3-4` : passage sur son tir a trois points en progres.
- Idee de reponse : Randle est decrit comme plus fiable car son jeu physique fonctionne, il lit mieux les prises a deux, defend mieux et apporte davantage au tir exterieur.

### Q02 - Pourquoi les Timberwolves impressionnent

- Question : Pourquoi les Timberwolves impressionnent-ils certains fans dans le fil Reddit ?
- Source attendue : `inputs/Reddit 1.pdf`.
- Emplacement dans le PDF :
  - `Reddit 1.pdf`, pages `10-11` : passage sur le plaisir de voir la serie Lakers/Wolves, Anthony Edwards, le jeu collectif et le manque de profondeur des Lakers.
  - `Reddit 1.pdf`, pages `12-13` : passage sur l'adaptation apres le trade de KAT et le roster des Wolves.
  - `Reddit 1.pdf`, pages `9-10` : contexte sur les equipes qui impressionnent et les limites de certains adversaires.
- Idee de reponse : Minnesota impressionne par son potentiel élevé, Anthony Edwards, une attaque plus collective et sa capacite a exposer le manque de profondeur des Lakers.

### Q03 - Surprises positives en playoffs

- Question : Quelles equipes reviennent le plus souvent comme surprises positives en playoffs, et pour quelles raisons ?
- Source attendue : `inputs/Reddit 1.pdf`.
- Emplacement dans le PDF :
  - `Reddit 1.pdf`, page `1` : debut du fil "Who are teams in the playoffs that have impressed you ?" et mention du Magic d'Orlando.
  - `Reddit 1.pdf`, pages `3-4` : discussion sur le Magic d'Orlando.
  - `Reddit 1.pdf`, pages `4-5` : mentions d'Indiana et Minnesota.
  - `Reddit 1.pdf`, pages `9-10` : mentions de Detroit et de son potentiel.
  - `Reddit 1.pdf`, pages `12-13` : autres mentions de Minnesota et Indiana.
- Idee de reponse : Les equipes qui ressortent sont surtout Orlando, Indiana, Minnesota et Detroit, pour leur jeune talent, leur progression, leur attaque ou leur equilibre.

### Q04 - Pacers sous-estimes par le public national

- Question : Pourquoi les Pacers peuvent-ils etre sous-estimes par le public national selon Reddit ?
- Source attendue : `inputs/Reddit 2.pdf`.
- Emplacement dans le PDF :
  - `Reddit 2.pdf`, pages `16-17` : passage indiquant que les Pacers avaient peu ou pas de matchs nationaux et que le public ne voit pas leurs comebacks.
  - `Reddit 2.pdf`, pages `18-19` : passage sur la narration mediatique et l'idee qu'une finale OKC/Pacers pourrait etre tres bonne.
  - `Reddit 2.pdf`, pages `20-21` : passage sur la capacite des Pacers a dicter le rythme et a ne pas etre sous-estimes.
- Idee de reponse : Les Pacers sont sous-estimes car ils ont manque d'exposition nationale ; beaucoup decouvrent tard leur rythme, leurs comebacks et leur qualite collective.

### Q05 - Finale OKC-Indiana ennuyeuse ou non

- Question : Franchement, OKC-Indiana en Finales, c'est vraiment le truc soporifique que certains annoncent ?
- Source attendue : `inputs/Reddit 2.pdf`.
- Emplacement dans le PDF :
  - `Reddit 2.pdf`, pages `18-19` : passage disant qu'une serie OKC/Pacers pourrait etre une des meilleures finales recentes.
  - `Reddit 2.pdf`, pages `20-21` : passage sur le rythme, le style de jeu et la capacite a dicter les matchs.
  - `Reddit 2.pdf`, pages `15-16` : passage sur les megathreads qui risquent d'etre toxiques.
- Idee de reponse : Non, le fil anticipe plutot une finale competitive et rapide, avec une reserve sur la toxicite possible des discussions en ligne.

### Q06 - Argument statistique pour Reggie Miller

- Question : Sur quoi repose l'argument statistique en faveur de Reggie Miller en playoffs ?
- Source attendue : `inputs/Reddit 3.pdf`.
- Emplacement dans le PDF :
  - `Reddit 3.pdf`, pages `2-3` : passage sur l'ecart statistique, le prime de Reggie et la comparaison avec d'autres scoreurs.
  - `Reddit 3.pdf`, pages `7-9` : tableau et rappel du post "Reggie Miller is the most efficient first option in NBA playoff history".
  - `Reddit 3.pdf`, pages `12-13` : passages sur sa longevite et sa regularite.
  - `Reddit 3.pdf`, pages `23-24` : rappel de l'argument autour de l'efficacite comme premiere option et des series gagnees.
- Idee de reponse : L'argument repose sur son relative true shooting ajuste a l'epoque, son prime 1991-2002, sa longevite et ses series gagnees sans coequipier Hall of Fame.

### Q07 - Avantage du terrain seulement en Finales

- Question : Une equipe NBA a-t-elle deja eu l'avantage du terrain seulement a partir des Finales ?
- Source attendue : `inputs/Reddit 4.pdf`.
- Emplacement dans le PDF :
  - `Reddit 4.pdf`, pages `1-2` : question du fil sur l'avantage du terrain jusqu'aux Finales.
  - `Reddit 4.pdf`, pages `6-7` : passage indiquant que ce n'est jamais arrive en NBA.
  - `Reddit 4.pdf`, pages `7-8` : passage expliquant que Miami 2023 ne marche pas car Denver avait l'avantage.
- Idee de reponse : Probablement aucune equipe en NBA moderne ; l'exemple Miami 2023 est ecarte parce que Denver avait l'avantage du terrain en Finales.

### Q08 - Meilleur pourcentage a trois points avec au moins 300 tentatives

- Question : Parmi les joueurs avec au moins 300 tirs a trois points tentes, qui a le meilleur pourcentage ?
- Source attendue : `inputs/regular NBA.xlsx`, feuille `Données NBA`.
- Emplacement dans la base SQLite :
  - Base : `database/nba.db`.
  - Table : `players`.
  - Colonnes utiles : `player_name`, `team_code`, `three_p_pct`, `three_pm`, `three_pa`.
- Requete logique :

```sql
SELECT player_name, team_code, three_p_pct, three_pm, three_pa
FROM players
WHERE three_pa >= 300
ORDER BY three_p_pct DESC
LIMIT 5;
```

- Resultat attendu en tete : `Zach LaVine`, `SAC`, `44.6`, `237` tirs marques, `533` tentatives.
- Idee de reponse : Zach LaVine a le meilleur pourcentage a trois points parmi les joueurs avec au moins 300 tentatives, avec 44,6 % sur 533 tentatives.

### Q09 - Plus grand total de rebonds

- Question : Quel joueur possede le plus grand total de rebonds dans la table des joueurs ?
- Source attendue : `inputs/regular NBA.xlsx`, feuille `Données NBA`.
- Emplacement dans la base SQLite :
  - Base : `database/nba.db`.
  - Table : `players`.
  - Colonnes utiles : `player_name`, `team_code`, `reb`.
- Requete logique :

```sql
SELECT player_name, team_code, reb
FROM players
ORDER BY reb DESC
LIMIT 5;
```

- Resultat attendu en tete : `Ivica Zubac`, `LAC`, `1008` rebonds.
- Idee de reponse : Ivica Zubac possede le plus grand total de rebonds avec 1008.

### Q10 - Meilleur pourcentage a trois points sur les cinq derniers matchs

- Question : Qui a le meilleur pourcentage a trois points sur ses cinq derniers matchs ?
- Sources attendues :
  - `inputs/regular NBA.xlsx`, feuille `Données NBA`.
  - `inputs/regular NBA.xlsx`, feuille `Dictionnaire des données`.
- Emplacement dans la base SQLite :
  - Base : `database/nba.db`.
  - Table principale : `players`.
  - Colonnes presentes liees au tir a trois points : `three_pm`, `three_pa`, `three_p_pct`.
  - Colonnes absentes : pas de `game_date`, pas de ligne match par match, pas de fenetre `last_5`, pas de statistique par cinq derniers matchs.
- Verification logique :

```sql
PRAGMA table_info(players);
```

- Ce que montre la source : les donnees sont des agregats de saison, pas des statistiques par match ou par fenetre temporelle.
- Idee de reponse : Impossible a etablir avec ces sources ; il faut refuser ou qualifier, car la donnee des cinq derniers matchs n'existe pas dans la base.
