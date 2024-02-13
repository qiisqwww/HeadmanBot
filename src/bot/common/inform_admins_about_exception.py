from aiogram import Bot
from aiogram.types import User
from loguru import logger

from src.bot.common.resources.templates import (
    something_went_wrong_for_admin_in_job_template,
    something_went_wrong_for_admin_template,
)
from src.modules.common.infrastructure.config.config import ADMIN_IDS

__all__ = [
    "inform_admins_about_exception",
    "inform_admins_about_job_exception",
]


async def inform_admins_about_exception(
    bot: Bot,
    exception: Exception,
    cause_by_student: User | None,
) -> None:
    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            something_went_wrong_for_admin_template(
                exception,
                cause_by_student,
            ),
        )
    logger.exception(exception)


async def inform_admins_about_job_exception(
    bot: Bot,
    exception: Exception,
    job_name: str,
) -> None:
    for admin_id in ADMIN_IDS:
        await bot.send_message(
            admin_id,
            something_went_wrong_for_admin_in_job_template(
                exception,
                job_name,
            ),
        )
    logger.exception(exception)
