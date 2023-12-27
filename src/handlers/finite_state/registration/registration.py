from datetime import date

from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.contexts import RegistrationContext
from src.enums import Role
from src.external.apis import ScheduleApi
from src.external.apis.schedule_api.exceptions import FailedToCheckGroupExistence
from src.handlers.finite_state.registration.validation import (
    is_valid_name_len,
    is_valid_surname_len,
)
from src.kernel import Router
from src.resources import (
    ASK_BIRTHDATE_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    BIRTHDATE_INCORRECT_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    asking_data_validation_template
)
from src.resources.buttons.inline_buttons import ask_fullname_validity_buttons
from src.resources.templates.templates import (
    TOO_MUCH_NAME_LENGTH_TEMPLATE,
    TOO_MUCH_SURNAME_LENGTH_TEMPLATE,
)
from src.services import GroupService, StudentService

from .registration_states import RegistrationStates

__all__ = [
    "registration_finite_state_router",
]

registration_finite_state_router = Router(
    must_be_registered=False,
)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_role)
@logger.catch
async def incorrect_student_role(message: Message) -> None:
    await message.answer(INCORRECT_STUDENT_ROLE_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_university)
@logger.catch
async def incorrect_university(message: Message) -> None:
    await message.answer(INCORRECT_UNIVERSITY_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_group)
@logger.catch
async def handling_group(
    message: Message,
    state: RegistrationContext,
    group_service: GroupService,
    student_service: StudentService,
) -> None:
    if message.text is None:
        return

    api = ScheduleApi(await state.university_alias)

    try:
        if not await api.group_exists(message.text):
            await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return
    except FailedToCheckGroupExistence:
        await message.answer(
            "Не удалось проверить наличие группы в университете, попробуйте снова или напишите в @noheadproblemsbot"
        )
        await state.set_state(RegistrationStates.waiting_group)
        return

    group = await group_service.find_by_name_and_uni(message.text, await state.university_alias)
    if await state.role == Role.STUDENT and group is None:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    if (
        group is not None
        and await state.role == Role.HEADMAN
        and await student_service.get_headman_by_group_name(group.name) is not None
    ):
        await message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    await state.set_group_name(message.text)
    await message.answer(ASK_BIRTHDATE_TEMPLATE)
    await state.set_state(RegistrationStates.waiting_birthdate)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthdate)
@logger.catch
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
@logger.catch
async def handling_surname(message: Message, state: RegistrationContext) -> None:
    if message.text is None:
        return

    if not is_valid_surname_len(message.text):
        await message.answer(TOO_MUCH_SURNAME_LENGTH_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_surname)
        return

    await state.set_surname(message.text)
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
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
        asking_data_validation_template(await state.surname, await state.name),
        reply_markup=ask_fullname_validity_buttons()
    )
    await state.set_state(RegistrationStates.ask_fullname_validity)
