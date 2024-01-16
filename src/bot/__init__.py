from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.modules.common.infrastructure.config.config import BOT_TOKEN
from src.modules.common.infrastructure.container import project_container

from .root_router import root_router

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dispatcher = Dispatcher(
    storage=MemoryStorage(),
    bot=bot,
    project_container=project_container,
)

dispatcher.include_router(root_router)


__all__ = [
    "dispatcher",
    "bot",
]
