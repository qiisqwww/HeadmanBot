from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import FSInputFile
from redis.asyncio import Redis

from src.modules.common.infrastructure import (
    DEBUG,
    WEBHOOK_SECRET,
    WEBHOOK_URL,
)
from src.modules.common.infrastructure.bot_notifier import BotNotifierImpl
from src.modules.common.infrastructure.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from src.modules.common.infrastructure.container import Container

from .build_root_router import build_root_router

__all__ = [
    "dispatcher",
    "init_bot_webhook",
]

WEBHOOK_SSL_CERT = "headman_bot.crt"


async def init_bot_webhook() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    if DEBUG:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    else:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET, certificate=FSInputFile(WEBHOOK_SSL_CERT))
    await bot.session.close()


dispatcher = Dispatcher(
    storage=RedisStorage(Redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True")),
    container=Container,
    notifier=BotNotifierImpl(),
)
dispatcher.include_router(build_root_router())
