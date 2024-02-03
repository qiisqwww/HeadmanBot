from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common.resources import main_menu, void_inline_buttons
from src.bot.common.router import RootRouter, Router
from src.modules.student_management.application.commands import (
    ClearCreateStudentDataCacheCommand,
    RegisterStudentCommand,
)

from ..callback_data import AccessCallbackData
from ..resources.templates import (
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
)

__all__ = [
    "include_access_callback_router",
]


access_callback_router = Router(
    must_be_registered=None,
)


def include_access_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(access_callback_router)


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
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=void_inline_buttons())
        await bot.send_message(callback_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    student = await register_student_command.execute(callback_data.telegram_id)

    await bot.send_message(callback_data.telegram_id, YOU_WERE_ACCEPTED_TEMPLATE, reply_markup=main_menu(student.role))
    await callback.message.edit_text(REGISTRATION_ACCEPTED_TEMPLATE, reply_markup=void_inline_buttons())
