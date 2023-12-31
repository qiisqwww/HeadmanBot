from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.contexts import RegistrationContext
from src.enums import TelegramCommand
from src.kernel import Router
from src.resources import (
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    role_buttons,
    start_message_template,
)
from src.resources.buttons.reply_buttons import restart_button

from src.handlers.states.registration_states import RegistrationStates

__all__ = [
    "start_command_router",
]

start_command_router = Router(must_be_registered=False)


@start_command_router.message(F.text == TelegramCommand.START)
@logger.catch
async def start_command(message: Message, state: RegistrationContext) -> None:
    if message.from_user is None:
        return

    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message, reply_markup=restart_button())

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_telegram_id(message.from_user.id)
    await state.set_state(RegistrationStates.waiting_role)
