from datetime import date

from aiogram import F
from aiogram.types import Message

from src.bot.common.contextes import ProfileUpdateContext
from src.modules.student_management.domain.enums import ProfileField, Role
from src.bot.profile.validation import is_valid_name_len, is_valid_surname_len
from src.bot.profile.profile_update_states import ProfileUpdateStates
from src.bot.common import RootRouter, Router
from src.bot.profile.resources.templates import (
    asking_name_validation_template,
    asking_surname_validation_template,
    asking_birthdate_validation_template,
    NEW_BIRTHDATE_INCORRECT_TEMPLATE
)
from src.bot.profile.resources.inline_buttons import is_field_correct_buttons

__all__ = ["include_profile_update_router"]


profile_update_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


def include_profile_update_router(root_router: RootRouter) -> None:
    root_router.include_router(profile_update_router)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_name)
async def new_name_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_name = message.text

    if is_valid_name_len(new_name):
        await message.answer(
            text=asking_name_validation_template(new_name),
            reply_markup=is_field_correct_buttons(ProfileField.NAME),
        )

        await state.set_new_data(new_name)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_surname)
async def new_surname_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_surname = message.text

    if is_valid_surname_len(new_surname):
        await message.answer(
            text=asking_surname_validation_template(new_surname),
            reply_markup=is_field_correct_buttons(ProfileField.SURNAME),
        )

        await state.set_new_data(new_surname)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_birthdate)
async def new_surname_handler(message: Message, state: ProfileUpdateContext) -> None:
    new_birthdate = message.text

    if message.text == "0":
        await state.set_new_data(None)
        await message.answer(
            text=asking_birthdate_validation_template("не указана"),
            reply_markup=is_field_correct_buttons(ProfileField.BIRTHDATE),
        )
    else:
        try:
            day, month, year = map(int, message.text.split("."))
            birthdate = date(year=year, month=month, day=day)
            await state.set_new_data(birthdate)

            await message.answer(
                text=asking_birthdate_validation_template(birthdate),
                reply_markup=is_field_correct_buttons(ProfileField.BIRTHDATE),
            )
        except Exception:
            await message.answer(NEW_BIRTHDATE_INCORRECT_TEMPLATE)
            await state.set_state(ProfileUpdateStates.waiting_new_birthdate)
            return