from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.models import Match

router = APIRouter()


class MatchCreate(BaseModel):
    game_id: int
    home_team: str
    away_team: str
    match_time: datetime | None = None


class MatchResult(BaseModel):
    home_score: int
    away_score: int


@router.post("/")
async def create_match(data: MatchCreate, db: AsyncSession = Depends(get_db)):
    match = Match(**data.model_dump())
    db.add(match)
    await db.commit()
    await db.refresh(match)
    return match


@router.get("/game/{game_id}")
async def get_game_matches(game_id: int, db: AsyncSession = Depends(get_db)):
    matches = await db.scalars(select(Match).where(Match.game_id == game_id))
    return list(matches)


@router.patch("/{match_id}/result")
async def set_result(match_id: int, data: MatchResult, db: AsyncSession = Depends(get_db)):
    match = await db.get(Match, match_id)
    match.home_score = data.home_score
    match.away_score = data.away_score
    match.is_finished = True
    await db.commit()
    return match
