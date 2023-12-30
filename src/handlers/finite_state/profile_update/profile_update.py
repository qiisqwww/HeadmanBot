from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.enums import Role, ProfileField
from src.handlers.states import ProfileUpdateStates
from src.handlers.finite_state.validation import (
    is_valid_surname_len,
    is_valid_name_len
)
from src.resources import (
    asking_name_validation_template,
    asking_surname_validation_template,
    is_field_correct_buttons
)
from src.dto.contexts import ProfileUpdateContext

__all__ = [
    "profile_update_router"
]


profile_update_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_surname)
@logger.catch
async def new_surname_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_surname = message.text

    if is_valid_surname_len(new_surname):
        await message.answer(
            text=asking_surname_validation_template(new_surname),
            reply_markup=is_field_correct_buttons(ProfileField.surname)
        )

        await state.set_name(new_surname)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_name)
@logger.catch
async def new_name_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_name = message.text

    if is_valid_name_len(new_name):
        await message.answer(
            text=asking_name_validation_template(new_name),
            reply_markup=is_field_correct_buttons(ProfileField.name)
        )

        await state.set_name(new_name)
        await state.set_state(ProfileUpdateStates.on_validation)
