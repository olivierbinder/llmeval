# TODO — Pipeline Excel vers SQLite

## Objectif

Transformer le fichier `regular NBA.xlsx` en une base SQLite unique :

```text
database/nba.db
```

Le chargement sera effectué une seule fois. La base pourra être supprimée et recréée en cas de besoin.

## Périmètre Excel

Feuilles utilisées :

| Feuille Excel | Destination |
|---|---|
| `Données NBA` | Table `players` |
| `Equipe` | Table `teams` |
| `Dictionnaire des données` | Table `features` |

Feuilles ignorées :

- `Analyse`
- `Analyse Vide`

## Structure retenue

```text
src/llmeval/
├── ingestion/
│   ├── load_excel_to_db.py
│   └── schemas.py
└── database/
    ├── connection.py
    └── models.py
```

Aucun repository, système de migrations ou module de normalisation séparé n’est nécessaire pour cette première version.

Une petite modification de `src/llmeval/utils/config.py` sera également nécessaire afin d’utiliser :

```python
DATABASE_FILE = "database/nba.db"
DATABASE_URL = "sqlite:///database/nba.db"
```

---

## Processus Excel → SQLite

### 1. Initialisation

- Vérifier que le fichier Excel existe.
- Créer le dossier `database/` s’il n’existe pas.
- Supprimer et recréer `nba.db` lors du chargement one shot.
- Initialiser les tables SQLAlchemy.

### 2. Lecture des feuilles

- Lire `Equipe`.
- Lire `Données NBA`.
- Lire `Dictionnaire des données`.
- Vérifier la présence des colonnes obligatoires.

### 3. Normalisation minimale

L’Excel étant propre, seules les transformations nécessaires à SQLite seront appliquées :

- suppression des espaces autour des textes ;
- conversion des cellules vides en `None` ;
- conversion des valeurs numériques ;
- transformation des noms de colonnes en noms SQL sûrs.

Exemples :

| Excel | SQLite |
|---|---|
| `Player` | `player_name` |
| `Team` | `team_code` |
| `FG%` | `fg_pct` |
| `3P%` | `three_p_pct` |
| `+ / -` | `plus_minus` |
| `AST/TO` | `ast_to` |
| `OREB%` | `oreb_pct` |

La même normalisation sera appliquée aux codes insérés dans `features.feature_code`.

### 4. Validation Pydantic

Valider chaque ligne avant insertion :

- code équipe non vide ;
- nom du joueur non vide ;
- âge et statistiques numériques ;
- valeurs obligatoires présentes ;
- équipe du joueur existante dans `teams` ;
- absence de doublon joueur/équipe ;
- pourcentages et statistiques cohérents avec le format attendu.

### 5. Insertion

Ordre d’insertion :

1. `teams`
2. `features`
3. `players`

L’ordre garantit que chaque `players.team_code` référence une équipe existante.

### 6. Contrôles après chargement

- comparer le nombre de lignes Excel et SQL ;
- vérifier qu’aucun joueur ne référence une équipe inconnue ;
- vérifier l’absence de doublons ;
- vérifier que les trois tables ne sont pas vides ;
- afficher un résumé du chargement ;
- exécuter quelques requêtes simples de contrôle.

---

# Scripts Python à écrire

## `database/connection.py`

Responsabilités :

- récupérer `DATABASE_URL` depuis la configuration ;
- créer le moteur SQLAlchemy SQLite ;
- créer la fabrique de sessions ;
- fournir une fonction ou un contexte de session réutilisable ;
- activer les clés étrangères SQLite.

Ce module sera ensuite réutilisable par le futur Tool LangChain SQL.

## `database/models.py`

Responsabilités :

- déclarer la base SQLAlchemy ;
- définir les modèles `Team`, `Player` et `Feature` ;
- définir les clés primaires, clés étrangères et contraintes ;
- exposer la création des tables.

## `ingestion/schemas.py`

Responsabilités :

- définir les modèles Pydantic d’import :
  - `TeamImport`
  - `PlayerImport`
  - `FeatureImport`
- convertir et valider les valeurs provenant d’Excel ;
- centraliser les règles simples de qualité des données.

## `ingestion/load_excel_to_db.py`

Responsabilités :

- orchestrer tout le chargement ;
- lire les trois feuilles Excel ;
- renommer les colonnes ;
- transformer les lignes en modèles Pydantic ;
- créer ou recréer `database/nba.db` ;
- insérer les données via SQLAlchemy ;
- effectuer les contrôles finaux ;
- afficher un bilan clair des lignes importées et rejetées.

---

# Schéma SQLite prévu

## Table `teams`

| Colonne | Type | Contraintes |
|---|---|---|
| `team_code` | TEXT | PK, non nul |
| `team_name` | TEXT | non nul |

Exemple :

```text
BOS | Boston Celtics
LAL | Los Angeles Lakers
```

## Table `features`

| Colonne | Type | Contraintes |
|---|---|---|
| `feature_code` | TEXT | PK, non nul |
| `description` | TEXT | non nul |

`feature_code` correspondra au nom SQL normalisé utilisé dans `players`.

Exemple :

```text
gp      | Nombre de matchs joués (Games Played)
fg_pct  | Pourcentage de réussite aux tirs
offrtg  | Efficacité offensive
```

Cette table permettra au futur agent SQL de consulter la signification métier des colonnes.

## Table `players`

### Identité et rattachement

| Colonne | Type | Contraintes |
|---|---|---|
| `player_id` | INTEGER | PK, auto-incrément |
| `player_name` | TEXT | non nul |
| `team_code` | TEXT | FK vers `teams.team_code`, non nul |
| `age` | INTEGER | nullable selon les données |

Contrainte recommandée :

```text
UNIQUE(player_name, team_code)
```

### Statistiques

Les colonnes suivantes seront stockées dans la table `players` :

```text
gp
w
l
min
pts
fgm
fga
fg_pct
[champ 15:00 à confirmer]
three_pa
three_p_pct
ftm
fta
ft_pct
oreb
dreb
reb
ast
tov
stl
blk
pf
fp
dd2
td3
plus_minus
offrtg
defrtg
netrtg
ast_pct
ast_to
ast_ratio
oreb_pct
dreb_pct
reb_pct
to_ratio
efg_pct
ts_pct
usg_pct
pace
pie
poss
```

Types recommandés :

- `INTEGER` : `gp`, `w`, `l`, `dd2`, `td3`
- `REAL` : moyennes, pourcentages, ratings, ratios et possessions

## Point à confirmer avant le codage

La colonne Excel `15:00`, située entre `FG%` et `3PA`, doit être vérifiée.

Dans les statistiques NBA classiques, cette position correspond souvent à `3PM` — tirs à trois points réussis — qu’Excel peut convertir automatiquement en heure `15:00`.

Il faudra confirmer s’il s’agit :

- de `3PM`, à enregistrer comme `three_pm` ;
- ou réellement de « minutes jouées après 15:00 », avec un autre nom SQL.

---

# Résultat attendu

Après exécution du pipeline :

```text
database/nba.db
├── teams
├── players
└── features
```

Cette base sera directement exploitable par `SQLDatabase` et le `SQLDatabaseToolkit` de LangChain pour :

- découvrir le schéma ;
- consulter les définitions de statistiques ;
- générer des requêtes SQL ;
- exécuter des calculs et classements sur les joueurs.
