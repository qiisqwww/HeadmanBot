from aiogram.types import Message

from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.common.contextes import RegistrationContext
from src.bot.common.router import RootRouter, Router

from ..registration_states import RegistrationStates
from ..resources import restart_button, role_buttons
from ..resources.templates import CHOOSE_STUDENT_ROLE_TEMPLATE, start_message_template

__all__ = [
    "include_restart_command_router",
]

restart_command_router = Router()


@restart_command_router.message(CommandFilter(TelegramCommand.RESTART))
async def restart_command(message: Message, state: RegistrationContext) -> None:
    if message.from_user is None:
        return

    await state.clear()
    start_message = start_message_template(message.from_user.last_name, message.from_user.first_name)
    await message.answer(start_message, reply_markup=restart_button())

    await message.answer(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=role_buttons())
    await state.set_state(RegistrationStates.waiting_role)


def include_restart_command_router(root_router: RootRouter) -> None:
    root_router.include_router(restart_command_router)
