# %% IMPORTS -----
from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from llmeval.database.connection import engine


# %% BASE -----
class Base(DeclarativeBase):
    pass


# %% MODELS -----
class Team(Base):
    __tablename__ = "teams"

    team_code: Mapped[str] = mapped_column(String, primary_key=True)
    team_name: Mapped[str] = mapped_column(String, nullable=False)

    players: Mapped[list["Player"]] = relationship(back_populates="team")


class Feature(Base):
    __tablename__ = "features"

    feature_code: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)


class Player(Base):
    __tablename__ = "players"
    __table_args__ = (UniqueConstraint("player_name", "team_code"),)

    player_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_name: Mapped[str] = mapped_column(String, nullable=False)
    team_code: Mapped[str] = mapped_column(
        String, ForeignKey("teams.team_code"), nullable=False
    )
    age: Mapped[int | None] = mapped_column(Integer)

    gp: Mapped[int] = mapped_column(Integer, nullable=False)
    w: Mapped[int] = mapped_column(Integer, nullable=False)
    losses: Mapped[int] = mapped_column("l", Integer, nullable=False)
    min: Mapped[float] = mapped_column(Float, nullable=False)
    pts: Mapped[int] = mapped_column(Integer, nullable=False)
    fgm: Mapped[int] = mapped_column(Integer, nullable=False)
    fga: Mapped[int] = mapped_column(Integer, nullable=False)
    fg_pct: Mapped[float] = mapped_column(Float, nullable=False)
    three_pm: Mapped[int] = mapped_column(Integer, nullable=False)
    three_pa: Mapped[int] = mapped_column(Integer, nullable=False)
    three_p_pct: Mapped[float] = mapped_column(Float, nullable=False)
    ftm: Mapped[int] = mapped_column(Integer, nullable=False)
    fta: Mapped[int] = mapped_column(Integer, nullable=False)
    ft_pct: Mapped[float] = mapped_column(Float, nullable=False)
    oreb: Mapped[int] = mapped_column(Integer, nullable=False)
    dreb: Mapped[int] = mapped_column(Integer, nullable=False)
    reb: Mapped[int] = mapped_column(Integer, nullable=False)
    ast: Mapped[int] = mapped_column(Integer, nullable=False)
    tov: Mapped[int] = mapped_column(Integer, nullable=False)
    stl: Mapped[int] = mapped_column(Integer, nullable=False)
    blk: Mapped[int] = mapped_column(Integer, nullable=False)
    pf: Mapped[int] = mapped_column(Integer, nullable=False)
    fp: Mapped[int] = mapped_column(Integer, nullable=False)
    dd2: Mapped[int] = mapped_column(Integer, nullable=False)
    td3: Mapped[int] = mapped_column(Integer, nullable=False)
    plus_minus: Mapped[float] = mapped_column(Float, nullable=False)
    offrtg: Mapped[float] = mapped_column(Float, nullable=False)
    defrtg: Mapped[float] = mapped_column(Float, nullable=False)
    netrtg: Mapped[float] = mapped_column(Float, nullable=False)
    ast_pct: Mapped[float] = mapped_column(Float, nullable=False)
    ast_to: Mapped[float] = mapped_column(Float, nullable=False)
    ast_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    oreb_pct: Mapped[float] = mapped_column(Float, nullable=False)
    dreb_pct: Mapped[float] = mapped_column(Float, nullable=False)
    reb_pct: Mapped[float] = mapped_column(Float, nullable=False)
    to_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    efg_pct: Mapped[float] = mapped_column(Float, nullable=False)
    ts_pct: Mapped[float] = mapped_column(Float, nullable=False)
    usg_pct: Mapped[float] = mapped_column(Float, nullable=False)
    pace: Mapped[float] = mapped_column(Float, nullable=False)
    pie: Mapped[float] = mapped_column(Float, nullable=False)
    poss: Mapped[int] = mapped_column(Integer, nullable=False)

    team: Mapped[Team] = relationship(back_populates="players")


# %% TABLES -----
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
