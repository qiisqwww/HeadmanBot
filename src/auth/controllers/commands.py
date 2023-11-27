from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message
from loguru import logger

from src.auth.resources.inline_buttons import role_buttons
from src.auth.resources.templates import (
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    start_message_template,
)
from src.common.middlewares import (
    CheckRegistrationMiddleware,
    InjectDBConnectionMiddleware,
)

from .registration_context import RegistrationContext
from .registration_states import RegistrationStates

registration_commands_router = Router()
registration_commands_router.message.outer_middleware(InjectDBConnectionMiddleware())
registration_commands_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@registration_commands_router.message(CommandStart())
@logger.catch
async def start_command(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.from_user is None:
        return

    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message)

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await registration_ctx.set_state(RegistrationStates.waiting_role)
