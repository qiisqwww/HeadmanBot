from aiogram import Bot
from aiogram.types import CallbackQuery
from loguru import logger

from src.kernel import Router
from src.resources.buttons import inline_void_button
from src.resources.buttons.main_menu import main_menu
from src.callback_data import AccessCallbackData
from src.resources import (
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
)
from src.services import CacheStudentService, StudentService

__all__ = [
    "access_callback_router",
]


access_callback_router = Router()


@access_callback_router.callback_query(AccessCallbackData.filter())
@logger.catch
async def accept_or_deny_callback(
    callback: CallbackQuery,
    callback_data: AccessCallbackData,
    bot: Bot,
    student_service: StudentService,
    cache_student_service: CacheStudentService,
) -> None:
    if callback.message is None:
        return

    student_data = await cache_student_service.pop_student_cache(callback_data.student_id)

    if not callback_data.accepted:
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=inline_void_button())
        await bot.send_message(student_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    await student_service.register_student(student_data)

    await bot.send_message(
        callback_data.student_id, YOU_WERE_ACCEPTED_TEMPLATE, reply_markup=main_menu(student_data.role)
    )
    await callback.message.edit_text(REGISTRATION_ACCEPTED_TEMPLATE, reply_markup=inline_void_button())
