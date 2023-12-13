from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.resources import role_buttons
from src.resources import (
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    start_message_template,
)

from ..finite_state.registration.registration_context import RegistrationContext
from ..finite_state.registration.registration_states import RegistrationStates

__all__ = [
    "start_command_router",
]

start_command_router = Router(
    must_be_registered=False,
)


@start_command_router.message(CommandStart())
@logger.catch
async def start_command(message: Message, state: RegistrationContext) -> None:
    if message.from_user is None:
        return

    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message)

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_state(RegistrationStates.waiting_role)
