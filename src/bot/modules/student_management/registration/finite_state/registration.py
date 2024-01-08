from datetime import date

from aiogram import F
from aiogram.types import Message

from src.bot.common.contextes import RegistrationContext

# from src.external.apis.schedule_api.exceptions import FailedToCheckGroupExistence
from src.bot.common.router import RootRouter, Router
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.student_management.domain import Role

from ...validation import is_valid_name_len
from ..registration_states import RegistrationStates
from ..resources.inline_buttons import ask_fullname_validity_buttons
from ..resources.templates import (
    ASK_BIRTHDATE_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    BIRTHDATE_INCORRECT_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    TOO_MUCH_NAME_LENGTH_TEMPLATE,
    TOO_MUCH_SURNAME_LENGTH_TEMPLATE,
    asking_fullname_validation_template,
)

__all__ = [
    "include_registration_finite_state_router",
]

registration_finite_state_router = Router()


def include_registration_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(registration_finite_state_router)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_role)
async def incorrect_student_role(message: Message) -> None:
    await message.answer(INCORRECT_STUDENT_ROLE_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_university)
async def incorrect_university(message: Message) -> None:
    await message.answer(INCORRECT_UNIVERSITY_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_group)
async def handling_group(
    message: Message,
    state: RegistrationContext,
    check_group_exists_in_uni_query: CheckGroupExistsInUniQuery,
    find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
    find_group_headman_query: FindGroupHeadmanQuery,
) -> None:
    if message.text is None:
        return

    group_name = message.text

    try:
        group_exists = await check_group_exists_in_uni_query.execute(group_name, await state.university_alias)
        if not group_exists:
            await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return
    except Exception:
        await message.answer(
            "Не удалось проверить наличие группы в университете, попробуйте снова или напишите в @noheadproblemsbot"
        )
        await state.set_state(RegistrationStates.waiting_group)
        return

    group = await find_group_by_name_and_alias_query.execute(group_name, await state.university_alias)
    if await state.role == Role.STUDENT and group is None:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    if group is not None and await state.role == Role.HEADMAN:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is not None:
            await message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return

    await state.set_group_name(group_name)
    await message.answer(ASK_BIRTHDATE_TEMPLATE)
    await state.set_state(RegistrationStates.waiting_birthdate)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthdate)
async def handling_birthmonth(message: Message, state: RegistrationContext) -> None:
    if message.text is None:
        return

    if message.text == "0":
        await state.set_birthday(None)
    else:
        try:
            day, month, year = map(int, message.text.split("."))
            birthdate = date(year=year, month=month, day=day)
            await state.set_birthday(birthdate)
        except Exception:
            await message.answer(BIRTHDATE_INCORRECT_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_birthdate)
            return

    await state.set_state(RegistrationStates.waiting_surname)
    await message.answer(ASK_SURNAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_surname)
async def handling_surname(message: Message, state: RegistrationContext) -> None:
    if message.text is None:
        return

    if not is_valid_name_len(message.text):
        await message.answer(TOO_MUCH_SURNAME_LENGTH_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_surname)
        return

    await state.set_surname(message.text)
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
async def handling_name(
    message: Message,
    state: RegistrationContext,
) -> None:
    if message.from_user is None:
        return

    if message.text is None:
        return

    if not is_valid_name_len(message.text):
        await message.answer(TOO_MUCH_NAME_LENGTH_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_name)
        return

    await state.set_name(message.text)

    await message.answer(
        asking_fullname_validation_template(await state.surname, await state.name),
        reply_markup=ask_fullname_validity_buttons(),
    )