from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.contexts import EditingContext
from src.resources import (
    ASK_SURNAME_TEMPLATE,
    TOO_MUCH_SURNAME_LENGTH_TEMPLATE,
    ASK_NAME_TEMPLATE,
    TOO_MUCH_NAME_LENGTH_TEMPLATE,
    asking_data_validation_template,
    ask_fullname_validity_buttons
)
from src.enums.role import Role
from .updater_states import UpdaterStates
from ..validation import (
    is_valid_name_len,
    is_valid_surname_len
)


from src.enums import TelegramCommand
from src.kernel import Router


__all__ = [
    "edit_profile_router",
]


edit_profile_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@edit_profile_router.message(F.text == TelegramCommand.EDIT_PROFILE)
@logger.catch
async def edit_profile_command(message: Message, state: EditingContext) -> None:
    await message.answer(ASK_SURNAME_TEMPLATE)
    await state.set_state(UpdaterStates.waiting_surname)


@edit_profile_router.message(F.text, UpdaterStates.waiting_surname)
@logger.catch
async def handling_surname(message: Message, state: EditingContext) -> None:
    if message.text is None:
        return

    if not is_valid_surname_len(message.text):
        await message.answer(TOO_MUCH_SURNAME_LENGTH_TEMPLATE)
        await state.set_state(UpdaterStates.waiting_surname)
        return

    await state.set_surname(message.text)
    await state.set_state(UpdaterStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@edit_profile_router.message(F.text, UpdaterStates.waiting_name)
@logger.catch
async def handling_name(
    message: Message,
    state: EditingContext,
) -> None:
    if message.from_user is None:
        return

    if message.text is None:
        return

    if not is_valid_name_len(message.text):
        await message.answer(TOO_MUCH_NAME_LENGTH_TEMPLATE)
        await state.set_state(UpdaterStates.waiting_name)
        return

    await state.set_name(message.text)

    await message.answer(
        asking_data_validation_template(await state.surname, await state.name),
        reply_markup=ask_fullname_validity_buttons(is_editing=True)
    )
