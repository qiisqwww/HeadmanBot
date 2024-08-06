from typing import final

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import User
from injector import inject
from loguru import logger

from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.common.infrastructure.config.config import ADMIN_IDS, BOT_TOKEN

from .templates import (
    something_went_wrong_for_admin_in_job_template,
    something_went_wrong_for_admin_template,
)

__all__ = [
    "BotNotifierImpl",
]

@final
class BotNotifierImpl(BotNotifier):
    _bot: Bot

    @inject
    def __init__(self) -> None:
        self._bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    async def notify_about_exception(self, exception: Exception, cause_by_student: User | None) -> None:
        for admin_id in ADMIN_IDS:
            await self._bot.send_message(
                admin_id,
                something_went_wrong_for_admin_template(
                    exception,
                    cause_by_student,
                ),
            )
        logger.exception(exception)

    async def notify_about_job_exception(self, exception: Exception, job_name: str) -> None:
        for admin_id in ADMIN_IDS:
            await self._bot.send_message(
                admin_id,
                something_went_wrong_for_admin_in_job_template(
                    exception,
                    job_name,
                ),
            )
        logger.exception(exception)
