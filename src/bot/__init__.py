from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.modules.common.infrastructure.config import BOT_TOKEN
from src.modules.common.infrastructure.container import project_container

from .build_root_router import build_root_router

__all__ = [
    "dispatcher",
    "bot",
]

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dispatcher = Dispatcher(
    storage=MemoryStorage(),
    project_container=project_container,
)
dispatcher.include_router(build_root_router())
