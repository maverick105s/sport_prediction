from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user")
    participations: Mapped[list["GameParticipant"]] = relationship(back_populates="user")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    invite_code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    creator: Mapped["User"] = relationship()
    participants: Mapped[list["GameParticipant"]] = relationship(back_populates="game")
    matches: Mapped[list["Match"]] = relationship(back_populates="game")


class GameParticipant(Base):
    __tablename__ = "game_participants"

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    game: Mapped["Game"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="participations")


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    home_team: Mapped[str] = mapped_column(String(64))
    away_team: Mapped[str] = mapped_column(String(64))
    match_time: Mapped[datetime | None] = mapped_column(DateTime)
    home_score: Mapped[int | None] = mapped_column(Integer)
    away_score: Mapped[int | None] = mapped_column(Integer)
    is_finished: Mapped[bool] = mapped_column(default=False)

    game: Mapped["Game"] = relationship(back_populates="matches")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="match")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    home_score: Mapped[int] = mapped_column(Integer)
    away_score: Mapped[int] = mapped_column(Integer)
    points: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    match: Mapped["Match"] = relationship(back_populates="predictions")
    user: Mapped["User"] = relationship(back_populates="predictions")
