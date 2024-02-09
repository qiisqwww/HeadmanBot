from datetime import date

from aiogram import F
from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ProfileUpdateContext
from src.bot.profile.profile_field import ProfileField
from src.bot.profile.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.inline_buttons import is_field_correct_buttons
from src.bot.profile.resources.templates import (
    NEW_BIRTHDATE_INCORRECT_TEMPLATE,
    asking_birthdate_validation_template,
    asking_name_validation_template,
    asking_surname_validation_template,
)
from src.bot.profile.validation import is_valid_name_len, is_valid_surname_len

__all__ = ["include_profile_update_router"]


profile_update_router = Router(
    must_be_registered=True,
)


def include_profile_update_router(root_router: RootRouter) -> None:
    root_router.include_router(profile_update_router)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_first_name)
async def new_name_handler(message: Message, state: ProfileUpdateContext) -> None:
    if message.text is None:
        return

    new_first_name = message.text
    if is_valid_name_len(new_first_name):
        await message.answer(
            text=asking_name_validation_template(new_first_name),
            reply_markup=is_field_correct_buttons(ProfileField.FIRST_NAME),
        )

        await state.set_new_first_name(new_first_name)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_last_name)
async def new_surname_handler(message: Message, state: ProfileUpdateContext) -> None:
    if message.text is None:
        return

    new_last_name = message.text
    if is_valid_surname_len(new_last_name):
        await message.answer(
            text=asking_surname_validation_template(new_last_name),
            reply_markup=is_field_correct_buttons(ProfileField.LAST_NAME),
        )

        await state.set_new_last_name(new_last_name)
        await state.set_state(ProfileUpdateStates.on_validation)


@profile_update_router.message(F.text, ProfileUpdateStates.waiting_new_birthdate)
async def new_birthdate_handler(message: Message, state: ProfileUpdateContext) -> None:
    if message.text is None:
        return

    new_birthdate = message.text
    valid_new_birthdate = None

    if new_birthdate != "0":
        try:
            day, month, year = map(int, new_birthdate.split("."))
            valid_new_birthdate = date(year=year, month=month, day=day)

        except Exception:
            await message.answer(NEW_BIRTHDATE_INCORRECT_TEMPLATE)
            await state.set_state(ProfileUpdateStates.waiting_new_birthdate)
            return

    await state.set_new_birthdate(valid_new_birthdate)
    await message.answer(
        text=asking_birthdate_validation_template(valid_new_birthdate),
        reply_markup=is_field_correct_buttons(ProfileField.BIRTHDATE),
    )
