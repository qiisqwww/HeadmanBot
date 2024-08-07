from aiogram.filters import or_f
from aiogram.types import Message

from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.common.contextes import RegistrationContext
from src.bot.common.router import RootRouter, Router
from src.bot.registration.finite_state.registration_states import RegistrationStates
from src.bot.registration.resources.inline_buttons import role_buttons
from src.bot.registration.resources.reply_buttons import restart_button
from src.bot.registration.resources.templates import CHOOSE_STUDENT_ROLE_TEMPLATE, start_message_template
from src.modules.student_management.application.commands import (
    ClearCreateStudentDataCacheIfExistsCommand,
)

__all__ = [
    "include_start_command_router",
]

start_command_router = Router()


@start_command_router.message(
    or_f(CommandFilter(TelegramCommand.START), CommandFilter(TelegramCommand.RESTART)),
)
async def start_command(
    message: Message,
    state: RegistrationContext,
    clear_cached_student_data_command: ClearCreateStudentDataCacheIfExistsCommand,
) -> None:
    if message.from_user is None:
        return

    await state.clear()
    await clear_cached_student_data_command.execute(message.from_user.id)

    start_message = start_message_template(
        message.from_user.last_name,
        message.from_user.first_name,
    )
    await message.answer(start_message, reply_markup=restart_button())

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_telegram_id(message.from_user.id)
    await state.set_state(RegistrationStates.waiting_role)


def include_start_command_router(root_router: RootRouter) -> None:
    root_router.include_router(start_command_router)
