from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import FSInputFile
from redis.asyncio import Redis

from src.common.bot_notifier import BotNotifier
from src.common.config import (
    WEBHOOK_SECRET,
    WEBHOOK_URL,
    BOT_TOKEN, REDIS_HOST, REDIS_PORT,
)
from src.common.database import create_db_pool
from .build_root_router import build_root_router

__all__ = [
    "dispatcher",
    "init_bot_webhook",
]

WEBHOOK_SSL_CERT = "headman_bot.pem"


async def init_bot_webhook() -> None:
    async with Bot(BOT_TOKEN) as bot:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(
            url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET, certificate=FSInputFile(WEBHOOK_SSL_CERT),
        )


dispatcher = Dispatcher(
    storage=RedisStorage(Redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True")),
    notifier=BotNotifier(),
    db_pool=create_db_pool(),
)
dispatcher.include_router(build_root_router())
