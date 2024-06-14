from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from aiogram.types import Update
from fastapi import FastAPI, Request

from src.bot import bot, dispatcher
from src.modules.common.infrastructure import (
    DEBUG,
    WEBHOOK_PATH,
    configure_logger,
)
from src.modules.common.infrastructure.build_scheduler import build_scheduler
from src.modules.common.infrastructure.container import Container

__all__ = [
    "app",
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    configure_logger()

    await Container.init(bot)
    # scheduler = await build_scheduler(bot)
    # scheduler.start()

    yield

    await bot.session.close()
    await Container.close()


app = FastAPI(debug=DEBUG, lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request) -> None:
    update = Update.model_validate_json(await request.body(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)
