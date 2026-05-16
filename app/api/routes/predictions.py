from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.models.models import Match, Prediction
from app.services.scoring import calculate_points

router = APIRouter()


class PredictionCreate(BaseModel):
    match_id: int
    user_id: int
    home_score: int
    away_score: int


@router.post("/")
async def make_prediction(data: PredictionCreate, db: AsyncSession = Depends(get_db)):
    # нельзя делать прогноз дважды
    existing = await db.scalar(
        select(Prediction).where(
            Prediction.match_id == data.match_id,
            Prediction.user_id == data.user_id,
        )
    )
    if existing:
        raise HTTPException(400, "Prediction already made")

    pred = Prediction(**data.model_dump())
    db.add(pred)
    await db.commit()
    await db.refresh(pred)
    return pred


@router.get("/match/{match_id}")
async def get_match_predictions(match_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Возвращает прогнозы других игроков только если текущий пользователь
    уже сделал свой прогноз.
    """
    user_pred = await db.scalar(
        select(Prediction).where(
            Prediction.match_id == match_id,
            Prediction.user_id == user_id,
        )
    )
    if not user_pred:
        raise HTTPException(403, "Make your prediction first")

    all_preds = await db.scalars(select(Prediction).where(Prediction.match_id == match_id))
    return list(all_preds)


@router.post("/finalize/{match_id}")
async def finalize_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Начислить очки после того как внесён результат матча."""
    match = await db.get(Match, match_id)
    if not match or not match.is_finished:
        raise HTTPException(400, "Match not finished")

    preds = await db.scalars(select(Prediction).where(Prediction.match_id == match_id))
    for pred in preds:
        pred.points = calculate_points(
            pred.home_score, pred.away_score,
            match.home_score, match.away_score,
        )
    await db.commit()
    return {"detail": "Points calculated"}
