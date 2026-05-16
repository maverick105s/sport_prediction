from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.models.models import User

router = APIRouter()


class UserUpsert(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None


@router.post("/upsert")
async def upsert_user(data: UserUpsert, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    user = await db.scalar(select(User).where(User.telegram_id == data.telegram_id))
    if not user:
        user = User(**data.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user
