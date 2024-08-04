from datetime import date

from aiogram import F
from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import RegistrationContext
from src.bot.registration.finite_state.registration_states import RegistrationStates
from src.bot.registration.resources.inline_buttons import ask_fullname_validity_buttons
from src.bot.registration.resources.templates import (
    ASK_BIRTHDATE_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    BIRTHDATE_INCORRECT_TEMPLATE,
    FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    TOO_MUCH_NAME_LENGTH_TEMPLATE,
    TOO_MUCH_SURNAME_LENGTH_TEMPLATE,
    asking_fullname_validation_template,
)
from src.bot.registration.validation import is_valid_name_len
from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.student_management.domain import Role
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

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
    notifier: BotNotifier,
) -> None:
    if message.text is None:
        return

    group_name = message.text

    try:
        group_exists = await check_group_exists_in_uni_query.execute(
            group_name,
            await state.university_alias,
        )
    except ScheduleApiError as e:
        await message.answer(FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        await notifier.notify_about_exception(e, message.from_user)
        return

    if not group_exists:
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    """Логика ниже была переработана для учета той ситуации, когда группа уже существует в базе, но студенты
    регистрируются в ней с нуля.
    Таким образом, старостой в группу МОЖНО зарегаться если группа существует,
    и нельзя только, если староста уже есть."""
    group = await find_group_by_name_and_alias_query.execute(
        group_name,
        await state.university_alias,
    )
    role = await state.role

    if group is not None and role == Role.HEADMAN:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is not None:
            await message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return

    if group is None and role == Role.STUDENT:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    if group is not None and role == Role.STUDENT:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is None:
            await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return

    await state.set_group_name(group_name)
    await message.answer(ASK_BIRTHDATE_TEMPLATE)
    await state.set_state(RegistrationStates.waiting_birthdate)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthdate)
async def handling_birth_month(message: Message, state: RegistrationContext) -> None:
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

    await state.set_last_name(message.text)
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
async def handling_name(
    message: Message,
    state: RegistrationContext,
) -> None:
    if message.from_user is None or message.text is None:
        return

    if not is_valid_name_len(message.text):
        await message.answer(TOO_MUCH_NAME_LENGTH_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_name)
        return

    await state.set_first_name(message.text)
    await state.set_state(RegistrationStates.ask_fullname_validity)

    await message.answer(
        asking_fullname_validation_template(
            await state.last_name,
            await state.first_name,
        ),
        reply_markup=ask_fullname_validity_buttons(),
    )
