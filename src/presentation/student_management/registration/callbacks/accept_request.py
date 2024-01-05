from aiogram import Bot
from aiogram.types import CallbackQuery

from src.application.student_management.commands import (
    ClearCreateStudentDataCacheCommand,
    RegisterStudentCommand,
)
from src.presentation.common.resources.main_menu import main_menu
from src.presentation.common.resources.void_inline_buttons import inline_void_button
from src.presentation.common.router import Router

from ..callback_data import AccessCallbackData
from ..resources.templates import (
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
)

__all__ = [
    "access_callback_router",
]


access_callback_router = Router(
    must_be_registered=False,
)


@access_callback_router.callback_query(AccessCallbackData.filter())
async def accept_or_deny_callback(
    callback: CallbackQuery,
    callback_data: AccessCallbackData,
    bot: Bot,
    clear_create_student_data_command: ClearCreateStudentDataCacheCommand,
    register_student_command: RegisterStudentCommand,
) -> None:
    if callback.message is None:
        return

    if not callback_data.accepted:
        await clear_create_student_data_command.execute(callback_data.telegram_id)
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=inline_void_button())
        await bot.send_message(callback_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    student = await register_student_command.execute(callback_data.telegram_id)

    await bot.send_message(callback_data.telegram_id, YOU_WERE_ACCEPTED_TEMPLATE, reply_markup=main_menu(student.role))
    await callback.message.edit_text(REGISTRATION_ACCEPTED_TEMPLATE, reply_markup=inline_void_button())
