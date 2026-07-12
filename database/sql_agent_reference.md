# SQL Agent Guide — NBA Database

## Base

SQLite database:

```text
database/nba.db
```

The SQL agent must answer numeric and statistical NBA questions by querying this database.

## Tables

### `teams`

One row per NBA team.

| Column | Meaning |
|---|---|
| `team_code` | Team code, for example `BOS`, `LAL`, `OKC` |
| `team_name` | Full team name |

### `players`

One row per player/team.

Important identity columns:

| Column | Meaning |
|---|---|
| `player_id` | Internal player row id |
| `player_name` | Player name |
| `team_code` | Team code, foreign key to `teams.team_code` |
| `age` | Player age |

Common statistical columns:

| Column | Meaning |
|---|---|
| `gp` | Games played |
| `w` | Wins |
| `l` | Losses |
| `min` | Minutes per game |
| `pts` | Points |
| `reb` | Rebounds |
| `ast` | Assists |
| `stl` | Steals |
| `blk` | Blocks |
| `tov` | Turnovers |
| `fg_pct` | Field goal percentage |
| `three_pm` | 3-point field goals made |
| `three_pa` | 3-point field goals attempted |
| `three_p_pct` | 3-point percentage |
| `ft_pct` | Free throw percentage |
| `plus_minus` | Plus-minus |
| `offrtg` | Offensive rating |
| `defrtg` | Defensive rating |
| `netrtg` | Net rating |
| `efg_pct` | Effective field goal percentage |
| `ts_pct` | True shooting percentage |
| `usg_pct` | Usage rate |
| `pace` | Pace |
| `pie` | Player impact estimate |
| `poss` | Possessions |

### `features`

Dictionary table for statistical columns.

| Column | Meaning |
|---|---|
| `feature_code` | SQL column name used in `players` |
| `description` | Business meaning of the feature |

Use `features` when the user asks what a metric means.

## SQL Agent Rules

- Generate only `SELECT` queries.
- Never use `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, or `CREATE`.
- Use `LIMIT` for ranking or exploratory queries.
- Join `teams` when the user asks for full team names.
- Query `features` when the user asks for the definition of a metric.
- Prefer explicit column names over `SELECT *`.
- If a column is ambiguous, inspect `features` before answering.

## Query Examples

### Top scorers

```sql
SELECT player_name, team_code, pts
FROM players
ORDER BY pts DESC
LIMIT 10;
```

### Best true shooting percentage

```sql
SELECT player_name, team_code, ts_pct
FROM players
WHERE gp >= 20
ORDER BY ts_pct DESC
LIMIT 10;
```

### Compare two players

```sql
SELECT player_name, team_code, pts, reb, ast, ts_pct, efg_pct
FROM players
WHERE player_name IN ('Nikola Jokić', 'Giannis Antetokounmpo');
```

### Team total points

```sql
SELECT t.team_name, SUM(p.pts) AS total_points
FROM players p
JOIN teams t ON t.team_code = p.team_code
GROUP BY t.team_name
ORDER BY total_points DESC
LIMIT 10;
```

### Average stats by team

```sql
SELECT t.team_name, AVG(p.pts) AS avg_pts, AVG(p.reb) AS avg_reb, AVG(p.ast) AS avg_ast
FROM players p
JOIN teams t ON t.team_code = p.team_code
GROUP BY t.team_name
ORDER BY avg_pts DESC
LIMIT 10;
```

### Metric definition

```sql
SELECT feature_code, description
FROM features
WHERE feature_code = 'efg_pct';
```

### Find available percentage metrics

```sql
SELECT feature_code, description
FROM features
WHERE feature_code LIKE '%_pct'
ORDER BY feature_code;
```

### Efficient high-usage players

```sql
SELECT player_name, team_code, usg_pct, ts_pct, pts
FROM players
WHERE gp >= 20
ORDER BY usg_pct DESC, ts_pct DESC
LIMIT 10;
```

## Notes

- `three_pm` corresponds to the Excel column accidentally formatted as `15:00`.
- Percentages are stored as numeric values like `63.7`, not `0.637`.
- `pts`, `reb`, `ast`, and most counting columns are season totals in this database.
