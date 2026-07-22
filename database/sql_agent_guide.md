# Guide Agent SQL

Utilise `database/nba.db` pour répondre aux questions NBA chiffrées avec SQL.

## Tables

- `players`: une ligne par joueur/equipe. Colonnes principales : `player_name`, `team_code`, `age`, `gp`, `pts`, `reb`, `ast`, `stl`, `blk`, `tov`, `fg_pct`, `three_pm`, `three_pa`, `three_p_pct`, `ft_pct`, `plus_minus`, `offrtg`, `defrtg`, `netrtg`, `efg_pct`, `ts_pct`, `usg_pct`, `pace`, `pie`, `poss`.
- `teams`: `team_code`, `team_name`.
- `features`: `feature_code`, `description`. Utilise cette table pour expliquer les metriques.

## Regles

- Genere uniquement des requetes `SELECT`.
- Ne modifie jamais la base.
- Utilise `LIMIT` pour les classements.
- Joins `teams` seulement si le nom complet des equipes est necessaire.
- Interroge `features` si le sens d'une metrique est ambigu.
- Les pourcentages sont stockes comme `63.7`, pas `0.637`.
- `three_pm` signifie tirs a 3 points reussis.

## Exemples

Question : Affiche les cinq joueurs avec le plus d'interceptions.

```sql
SELECT player_name, team_code, stl
FROM players
ORDER BY stl DESC
LIMIT 5;
```

Question : Parmi les joueurs avec au moins 60 matchs joues, quels sont les meilleurs true shooting percentages ?

```sql
SELECT player_name, team_code, ts_pct, gp
FROM players
WHERE gp >= 60
ORDER BY ts_pct DESC
LIMIT 5;
```

Question : Donne le top 5 des joueurs aux contres avec le nom complet de leur equipe.

```sql
SELECT p.player_name, t.team_name, p.blk
FROM players p
JOIN teams t ON t.team_code = p.team_code
ORDER BY p.blk DESC
LIMIT 5;
```

Question : Explique la metrique usg_pct avec le dictionnaire des donnees.

```sql
SELECT feature_code, description
FROM features
WHERE feature_code = 'usg_pct';
```
