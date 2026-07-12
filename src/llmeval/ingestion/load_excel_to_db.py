# %% IMPORTS -----
import argparse
import re
import unicodedata
from datetime import time
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import ValidationError
from sqlalchemy import func, select, text

from llmeval.database.connection import engine, get_session
from llmeval.database.models import Feature, Player, Team, create_tables
from llmeval.ingestion.schemas import FeatureImport, PlayerImport, TeamImport
from llmeval.utils.config import DATABASE_FILE


# %% CONSTANTS -----
DEFAULT_EXCEL_PATH = Path("inputs/regular NBA.xlsx")
DATABASE_PATH = Path(DATABASE_FILE)

TEAM_COLUMNS = {
    "Code": "team_code",
    "Nom complet de l'equipe": "team_name",
    "Nom complet de l'équipe": "team_name",
}

FEATURE_SOURCE_COLUMN = "Dictionnaire des données"
FEATURE_DESCRIPTION_COLUMN = "Unnamed: 1"

REQUIRED_PLAYER_COLUMNS = [
    "Player",
    "Team",
    "Age",
    "GP",
    "W",
    "L",
    "Min",
    "PTS",
    "FGM",
    "FGA",
    "FG%",
    time(15, 0),
    "3PA",
    "3P%",
    "FTM",
    "FTA",
    "FT%",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "TOV",
    "STL",
    "BLK",
    "PF",
    "FP",
    "DD2",
    "TD3",
    "+/-",
    "OFFRTG",
    "DEFRTG",
    "NETRTG",
    "AST%",
    "AST/TO",
    "AST RATIO",
    "OREB%",
    "DREB%",
    "REB%",
    "TO RATIO",
    "EFG%",
    "TS%",
    "USG%",
    "PACE",
    "PIE",
    "POSS",
]

SPECIAL_COLUMN_NAMES = {
    "Player": "player_name",
    "Team": "team_code",
    "FG%": "fg_pct",
    "3PM": "three_pm",
    "3PA": "three_pa",
    "3P%": "three_p_pct",
    "+/-": "plus_minus",
    "+ / -": "plus_minus",
    "AST/TO": "ast_to",
}


# %% COLUMN NORMALIZATION -----
def strip_accents(value: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def clean_column_label(value: Any) -> str:
    if isinstance(value, time):
        return "3PM"
    label = str(value).strip()
    if label in {"15:00", "15:00:00"}:
        return "3PM"
    return label


def normalize_column_name(value: Any) -> str:
    label = clean_column_label(value)
    if label in SPECIAL_COLUMN_NAMES:
        return SPECIAL_COLUMN_NAMES[label]

    label = strip_accents(label).lower()
    label = label.replace("%", "_pct")
    label = label.replace("+", "plus")
    label = label.replace("-", "minus")
    label = re.sub(r"[^a-z0-9]+", "_", label)
    label = re.sub(r"_+", "_", label).strip("_")

    if label.startswith("3p"):
        label = "three_p" + label[2:]
    return label


def drop_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(axis=1, how="all")


def require_columns(df: pd.DataFrame, required: list[Any], sheet_name: str) -> None:
    missing = [clean_column_label(column) for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans {sheet_name}: {missing}")


# %% EXCEL READERS -----
def read_teams(excel_path: Path) -> list[TeamImport]:
    df = pd.read_excel(excel_path, sheet_name="Equipe")
    require_columns(df, ["Code", "Nom complet de l'équipe"], "Equipe")
    df = df.rename(columns=TEAM_COLUMNS)
    return [TeamImport.model_validate(row) for row in df.to_dict("records")]


def read_features(excel_path: Path) -> list[FeatureImport]:
    df = pd.read_excel(excel_path, sheet_name="Dictionnaire des données")
    require_columns(
        df,
        [FEATURE_SOURCE_COLUMN, FEATURE_DESCRIPTION_COLUMN],
        "Dictionnaire des donnees",
    )

    features = []
    for row in df.to_dict("records"):
        source_code = row[FEATURE_SOURCE_COLUMN]
        feature_code = normalize_column_name(source_code)
        description = row[FEATURE_DESCRIPTION_COLUMN]
        if feature_code == "three_pm":
            description = "Tirs a 3 points reussis par match (3PM)"
        features.append(
            FeatureImport.model_validate(
                {"feature_code": feature_code, "description": description}
            )
        )
    return features


def read_players(excel_path: Path, team_codes: set[str]) -> list[PlayerImport]:
    df = pd.read_excel(excel_path, sheet_name="Données NBA", header=1)
    df = drop_empty_columns(df)
    require_columns(df, REQUIRED_PLAYER_COLUMNS, "Donnees NBA")
    df = df.rename(columns={column: normalize_column_name(column) for column in df.columns})

    players = []
    seen_players = set()
    errors = []

    for index, row in enumerate(df.to_dict("records"), start=3):
        try:
            player = PlayerImport.model_validate(row)
            player_key = (player.player_name, player.team_code)
            if player.team_code not in team_codes:
                raise ValueError(f"equipe inconnue: {player.team_code}")
            if player_key in seen_players:
                raise ValueError(f"doublon joueur/equipe: {player_key}")
            seen_players.add(player_key)
            players.append(player)
        except (ValidationError, ValueError) as error:
            errors.append(f"ligne {index}: {error}")

    if errors:
        preview = "\n".join(errors[:10])
        raise ValueError(
            f"{len(errors)} ligne(s) joueur rejettee(s):\n{preview}"
        )
    return players


# %% DATABASE INITIALIZATION -----
def recreate_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    engine.dispose()
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
    create_tables()


# %% INSERTION -----
def insert_data(
    teams: list[TeamImport],
    features: list[FeatureImport],
    players: list[PlayerImport],
) -> None:
    with get_session() as session:
        session.add_all([Team(**team.model_dump()) for team in teams])
        session.add_all([Feature(**feature.model_dump()) for feature in features])
        session.add_all([Player(**player.model_dump()) for player in players])


# %% FINAL CHECKS -----
def count_rows(model: type[Team] | type[Feature] | type[Player]) -> int:
    with get_session() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


def run_checks(
    expected_teams: int,
    expected_features: int,
    expected_players: int,
) -> dict[str, int]:
    counts = {
        "teams": count_rows(Team),
        "features": count_rows(Feature),
        "players": count_rows(Player),
    }

    expected_counts = {
        "teams": expected_teams,
        "features": expected_features,
        "players": expected_players,
    }
    for table_name, expected_count in expected_counts.items():
        if counts[table_name] != expected_count:
            raise ValueError(
                f"Table {table_name}: {counts[table_name]} ligne(s), attendu {expected_count}"
            )
        if counts[table_name] == 0:
            raise ValueError(f"Table {table_name} vide")

    with get_session() as session:
        unknown_team_count = session.scalar(
            text(
                """
                SELECT COUNT(*)
                FROM players p
                LEFT JOIN teams t ON t.team_code = p.team_code
                WHERE t.team_code IS NULL
                """
            )
        )
        duplicate_count = session.scalar(
            text(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT player_name, team_code
                    FROM players
                    GROUP BY player_name, team_code
                    HAVING COUNT(*) > 1
                )
                """
            )
        )
        if unknown_team_count:
            raise ValueError(f"{unknown_team_count} joueur(s) avec equipe inconnue")
        if duplicate_count:
            raise ValueError(f"{duplicate_count} doublon(s) joueur/equipe")

    return counts


def print_summary(counts: dict[str, int]) -> None:
    print("Chargement termine")
    print(f"- Base SQLite: {DATABASE_PATH}")
    print(f"- Equipes importees: {counts['teams']}")
    print(f"- Features importees: {counts['features']}")
    print(f"- Joueurs importes: {counts['players']}")

    with get_session() as session:
        top_players = session.execute(
            text(
                """
                SELECT player_name, team_code, pts
                FROM players
                ORDER BY pts DESC
                LIMIT 5
                """
            )
        ).fetchall()

    print("- Top 5 points:")
    for player_name, team_code, pts in top_players:
        print(f"  {player_name} ({team_code}) - {pts}")


# %% PIPELINE -----
def load_excel_to_db(excel_path: Path = DEFAULT_EXCEL_PATH) -> None:
    if not excel_path.exists():
        raise FileNotFoundError(f"Fichier Excel introuvable: {excel_path}")

    teams = read_teams(excel_path)
    team_codes = {team.team_code for team in teams}
    features = read_features(excel_path)
    players = read_players(excel_path, team_codes)

    recreate_database()
    insert_data(teams, features, players)
    counts = run_checks(len(teams), len(features), len(players))
    print_summary(counts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Charge regular NBA.xlsx vers SQLite")
    parser.add_argument(
        "--excel-path",
        type=Path,
        default=DEFAULT_EXCEL_PATH,
        help=f"Chemin du fichier Excel (defaut: {DEFAULT_EXCEL_PATH})",
    )
    args = parser.parse_args()
    load_excel_to_db(args.excel_path)


if __name__ == "__main__":
    main()
