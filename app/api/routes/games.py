import random
import string

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Game, GameParticipant
from pydantic import BaseModel

router = APIRouter()


class GameCreate(BaseModel):
    name: str
    creator_id: int


class GameJoin(BaseModel):
    user_id: int


def _random_code(n=8) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


@router.post("/")
async def create_game(data: GameCreate, db: AsyncSession = Depends(get_db)):
    game = Game(name=data.name, creator_id=data.creator_id, invite_code=_random_code())
    db.add(game)
    # автоматически добавляем создателя как участника
    await db.flush()
    db.add(GameParticipant(game_id=game.id, user_id=data.creator_id))
    await db.commit()
    await db.refresh(game)
    return game


@router.post("/{invite_code}/join")
async def join_game(invite_code: str, data: GameJoin, db: AsyncSession = Depends(get_db)):
    game = await db.scalar(select(Game).where(Game.invite_code == invite_code))
    if not game:
        raise HTTPException(404, "Game not found")

    existing = await db.scalar(
        select(GameParticipant).where(
            GameParticipant.game_id == game.id,
            GameParticipant.user_id == data.user_id,
        )
    )
    if existing:
        return {"detail": "Already joined"}

    db.add(GameParticipant(game_id=game.id, user_id=data.user_id))
    await db.commit()
    return {"detail": "Joined", "game_id": game.id}


@router.get("/{game_id}/leaderboard")
async def leaderboard(game_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import func
    from app.models.models import Prediction, User

    rows = await db.execute(
        select(User.username, User.first_name, func.sum(Prediction.points).label("total"))
        .join(Prediction, Prediction.user_id == User.id)
        .join(Game, Game.id == game_id)
        .group_by(User.id)
        .order_by(func.sum(Prediction.points).desc())
    )
    return [{"user": r.username or r.first_name, "points": r.total or 0} for r in rows]
