from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from aiogram.types import FSInputFile, Update
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

WEBHOOK_SSL_CERT = "headman_bot.crt"

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    await bot.delete_webhook(drop_pending_updates=True)
    if DEBUG:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    else:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET, certificate=FSInputFile(WEBHOOK_SSL_CERT))


    yield

    await bot.session.close()


app = FastAPI(debug=DEBUG, lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request) -> None:
    update = Update.model_validate_json(await request.body(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)
