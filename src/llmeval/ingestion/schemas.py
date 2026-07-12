# %% IMPORTS -----
import math
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# %% COMMON HELPERS -----
def empty_to_none(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def parse_int(value: Any) -> int | None:
    value = empty_to_none(value)
    if value is None:
        return None
    number = float(value)
    if not number.is_integer():
        raise ValueError("expected an integer value")
    return int(number)


def parse_float(value: Any) -> float | None:
    value = empty_to_none(value)
    if value is None:
        return None
    return float(value)


# %% TEAM IMPORT -----
class TeamImport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    team_code: str
    team_name: str

    @field_validator("team_code", mode="before")
    @classmethod
    def clean_team_code(cls, value: Any) -> str:
        value = empty_to_none(value)
        if value is None:
            raise ValueError("team code must not be empty")
        return str(value).strip().upper()

    @field_validator("team_name", mode="before")
    @classmethod
    def clean_team_name(cls, value: Any) -> str:
        value = empty_to_none(value)
        if value is None:
            raise ValueError("team name must not be empty")
        return str(value).strip()


# %% FEATURE IMPORT -----
class FeatureImport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feature_code: str
    description: str

    @field_validator("feature_code", "description", mode="before")
    @classmethod
    def text_must_not_be_empty(cls, value: Any) -> str:
        value = empty_to_none(value)
        if value is None:
            raise ValueError("text field must not be empty")
        return str(value).strip()


# %% PLAYER IMPORT -----
class PlayerImport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    player_name: str
    team_code: str
    age: int | None
    gp: int
    w: int
    losses: int = Field(validation_alias="l")
    min: float
    pts: int
    fgm: int
    fga: int
    fg_pct: float
    three_pm: int
    three_pa: int
    three_p_pct: float
    ftm: int
    fta: int
    ft_pct: float
    oreb: int
    dreb: int
    reb: int
    ast: int
    tov: int
    stl: int
    blk: int
    pf: int
    fp: int
    dd2: int
    td3: int
    plus_minus: float
    offrtg: float
    defrtg: float
    netrtg: float
    ast_pct: float
    ast_to: float
    ast_ratio: float
    oreb_pct: float
    dreb_pct: float
    reb_pct: float
    to_ratio: float
    efg_pct: float
    ts_pct: float
    usg_pct: float
    pace: float
    pie: float
    poss: int

    @field_validator("player_name", mode="before")
    @classmethod
    def clean_player_name(cls, value: Any) -> str:
        value = empty_to_none(value)
        if value is None:
            raise ValueError("player name must not be empty")
        return str(value).strip()

    @field_validator("team_code", mode="before")
    @classmethod
    def clean_team_code(cls, value: Any) -> str:
        value = empty_to_none(value)
        if value is None:
            raise ValueError("team code must not be empty")
        return str(value).strip().upper()

    @field_validator(
        "age",
        "gp",
        "w",
        "losses",
        "pts",
        "fgm",
        "fga",
        "three_pm",
        "three_pa",
        "ftm",
        "fta",
        "oreb",
        "dreb",
        "reb",
        "ast",
        "tov",
        "stl",
        "blk",
        "pf",
        "fp",
        "dd2",
        "td3",
        "poss",
        mode="before",
    )
    @classmethod
    def clean_int(cls, value: Any) -> int | None:
        return parse_int(value)

    @field_validator(
        "min",
        "fg_pct",
        "three_p_pct",
        "ft_pct",
        "plus_minus",
        "offrtg",
        "defrtg",
        "netrtg",
        "ast_pct",
        "ast_to",
        "ast_ratio",
        "oreb_pct",
        "dreb_pct",
        "reb_pct",
        "to_ratio",
        "efg_pct",
        "ts_pct",
        "usg_pct",
        "pace",
        "pie",
        mode="before",
    )
    @classmethod
    def clean_float(cls, value: Any) -> float | None:
        return parse_float(value)
