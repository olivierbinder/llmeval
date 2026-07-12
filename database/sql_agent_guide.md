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

Question : Quel joueur a marque le plus de points ?

```sql
SELECT player_name, team_code, pts
FROM players
ORDER BY pts DESC
LIMIT 1;
```

Question : Parmi les joueurs avec au moins 300 tentatives a trois points, qui a le meilleur pourcentage a trois points ?

```sql
SELECT player_name, team_code, three_p_pct, three_pa
FROM players
WHERE three_pa >= 300
ORDER BY three_p_pct DESC
LIMIT 5;
```

Question : Quel joueur a le plus grand total de rebonds ?

```sql
SELECT player_name, team_code, reb
FROM players
ORDER BY reb DESC
LIMIT 5;
```

Question : Que signifie efg_pct ?

```sql
SELECT feature_code, description
FROM features
WHERE feature_code = 'efg_pct';
```
