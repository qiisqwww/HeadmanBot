from aiogram import F
from aiogram.types import Message

from src.dto.contexts import ProfileUpdateContext
from src.enums import ProfileField, Role
from src.handlers.finite_state.validation import is_valid_name_len, is_valid_surname_len
from src.handlers.states import ProfileUpdateStates
from src.kernel import Router
from src.resources import (
    asking_name_validation_template,
    asking_surname_validation_template,
    is_field_correct_buttons,
)

__all__ = ["profile_update_router"]


profile_update_router = Router(must_be_registered=True, minimum_role=Role.STUDENT)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_surname)
async def new_surname_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_surname = message.text

    if is_valid_surname_len(new_surname):
        await message.answer(
            text=asking_surname_validation_template(new_surname),
            reply_markup=is_field_correct_buttons(ProfileField.surname),
        )

        await state.set_surname(new_surname)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_name)
async def new_name_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_name = message.text

    if is_valid_name_len(new_name):
        await message.answer(
            text=asking_name_validation_template(new_name), reply_markup=is_field_correct_buttons(ProfileField.name)
        )

        await state.set_name(new_name)
        await state.set_state(ProfileUpdateStates.on_validation)
