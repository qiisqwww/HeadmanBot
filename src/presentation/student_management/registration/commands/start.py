from aiogram.types import Message

from src.presentation.common.command_filter import CommandFilter, TelegramCommand
from src.presentation.common.router import Router

from ..registration_context import RegistrationContext
from ..registration_states import RegistrationStates
from ..resources import restart_button, role_buttons
from ..resources.templates import CHOOSE_STUDENT_ROLE_TEMPLATE, start_message_template

__all__ = [
    "start_command_router",
]

start_command_router = Router(must_be_registered=False)


@start_command_router.message(CommandFilter(TelegramCommand.START))
async def start_command(message: Message, state: RegistrationContext) -> None:
    if message.from_user is None:
        return

    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message, reply_markup=restart_button())

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_telegram_id(message.from_user.id)
    await state.set_state(RegistrationStates.waiting_role)
