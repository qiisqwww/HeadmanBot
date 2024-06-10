from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.modules.common.infrastructure.bot_notifier import BotNotifierImpl
from src.modules.common.infrastructure.config import BOT_TOKEN
from src.modules.common.infrastructure.container import Container

from .root_router import build_root_router

__all__ = [
    "dispatcher",
    "bot",
]

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)


dispatcher = Dispatcher(
    storage=MemoryStorage(),
    container=Container,
    notifier=BotNotifierImpl(bot),
)
dispatcher.include_router(build_root_router())
