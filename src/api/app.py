from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, Request

from src.bot import bot, dispatcher
from src.modules.common.infrastructure import (
    DEBUG,
    WEBHOOK_PATH,
    WEBHOOK_SECRET,
    WEBHOOK_URL,
)

__all__ = [
    "app",
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

    yield

    await bot.session.close()


app = FastAPI(debug=DEBUG, lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update = Update.model_validate_json(await request.body(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)
