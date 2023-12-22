from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.contexts import RegistrationContext
from src.kernel import Router
from src.resources import (
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    role_buttons,
    start_message_template,
)
from src.resources.buttons.reply_buttons import restart_button

from ..finite_state.registration.registration_states import RegistrationStates

__all__ = [
    "restart_command_router",
]

restart_command_router = Router(must_be_registered=False)


@restart_command_router.message(F.text == "Начать регистрацию заново")
@logger.catch
async def restart_command(message: Message, state: RegistrationContext) -> None:
    if message.from_user is None:
        return

    await state.clear()
    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message, reply_markup=restart_button())

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_state(RegistrationStates.waiting_role)
