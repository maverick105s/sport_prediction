import asyncio
import logging

from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.models import User, Game, GameParticipant
from sqlalchemy import select
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_or_create_user(telegram_user) -> User:
    async with AsyncSessionLocal() as db:
        user = await db.scalar(
            select(User).where(User.telegram_id == telegram_user.id)
        )
        if not user:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_user(update.effective_user)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🏒 Открыть игру",
            web_app=WebAppInfo(url=f"{settings.webapp_url}?game_id=1")
        )],
    ])

    await update.message.reply_text(
        "Чтобы создать игру напиши:\n`/newgame Название игры`\n\nЧтобы войти в игру:\n`/join КОД`",
        parse_mode="Markdown",
    )

    await update.message.reply_text(
        f"Привет, {user.first_name or 'друг'}! 👋\n\n"
        "Делай прогнозы на матчи и соревнуйся с друзьями.\n\n"
        "🏆 Система очков:\n"
        "3 — точный счёт\n"
        "2 — правильная разница\n"
        "1 — правильный исход\n",
        reply_markup=keyboard,
    )


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Укажи название игры:\n/newgame Плей-офф 2026"
        )
        return

    name = " ".join(context.args)
    tg_user = update.effective_user

    async with AsyncSessionLocal() as db:
        user = await db.scalar(select(User).where(User.telegram_id == tg_user.id))
        if not user:
            user = await get_or_create_user(tg_user)

        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        game = Game(name=name, creator_id=user.id, invite_code=code)
        db.add(game)
        await db.flush()
        db.add(GameParticipant(game_id=game.id, user_id=user.id))
        await db.commit()

    await update.message.reply_text(
        f"✅ Игра *{name}* создана!\n\n"
        f"Код для приглашения: `{code}`\n\n"
        "Отправь друзьям команду:\n"
        f"`/join {code}`",
        parse_mode="Markdown",
    )


async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи код игры:\n/join ABC12345")
        return

    code = context.args[0].upper()
    tg_user = update.effective_user

    async with AsyncSessionLocal() as db:
        game = await db.scalar(select(Game).where(Game.invite_code == code))
        if not game:
            await update.message.reply_text("❌ Игра не найдена. Проверь код.")
            return

        user = await db.scalar(select(User).where(User.telegram_id == tg_user.id))
        if not user:
            user = await get_or_create_user(tg_user)

        existing = await db.scalar(
            select(GameParticipant).where(
                GameParticipant.game_id == game.id,
                GameParticipant.user_id == user.id,
            )
        )
        if existing:
            await update.message.reply_text("Ты уже в этой игре!")
            return

        db.add(GameParticipant(game_id=game.id, user_id=user.id))
        await db.commit()

    await update.message.reply_text(
        f"🎉 Ты присоединился к игре *{game.name}*!",
        parse_mode="Markdown",
    )


def main():
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("newgame", new_game))
    app.add_handler(CommandHandler("join", join_game))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
