from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI, Request

from src.bot import dispatcher
from src.common.config import (
    BOT_TOKEN,
    DEBUG,
    WEBHOOK_PATH,
    configure_logger,
)

__all__ = [
    "app",
]

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    configure_logger()

    yield

    await bot.session.close()


app = FastAPI(debug=DEBUG, lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request) -> None:
    update = Update.model_validate_json(await request.body(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)
