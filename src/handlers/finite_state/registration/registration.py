from datetime import date

from aiogram import Bot, F
from aiogram.types import Message
from loguru import logger

from src.config import ADMIN_IDS
from src.dto import StudentId
from src.enums import Role
from src.external.apis import ScheduleApi
from src.handlers.finite_state.registration.registration_context import (
    RegistrationContext,
)
from src.handlers.finite_state.registration.registration_states import (
    RegistrationStates,
)
from src.kernel import Router
from src.resources.buttons.inline_buttons import accept_or_deny_buttons
from src.resources.templates.templates import (
    ASK_BIRTHDATE_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    BIRTHDATE_INCORRECT_TEMPLATE,
    GROUP_ALREADY_HAS_A_HEADMAN,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
)
from src.services.interfaces.group_service_interface import GroupService
from src.services.interfaces.student_service_interface import StudentService

__all__ = [
    "registration_finite_state_router",
]

registration_finite_state_router = Router()


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

    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    group = await group_service.find_by_name_and_uni(message.text, await state.university_alias)
    if await state.role == Role.STUDENT and group is None:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    if group is not None and await state.role == Role.HEADMAN and await student_service.group_has_headman(group.id):
        await message.answer(GROUP_ALREADY_HAS_A_HEADMAN)
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

    await state.set_surname(message.text)
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
async def handling_name(
    message: Message,
    state: RegistrationContext,
    bot: Bot,
    student_service: StudentService,
    cache_student_service: CacheStudentService,
) -> None:
    if message.from_user is None:
        return

    if message.text is None:
        return

    await state.set_name(message.text)
    await state.set_telegram_id(message.from_user.id)
    await state.set_state(RegistrationStates.on_verification)

    match await state.role:
        case Role.STUDENT:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    student_data = await state.get_data()
    student_id = await state.telegram_id
    await cache_student_service.cache_student(student_data)

    if await state.role == Role.HEADMAN:
        surname = await state.surname
        name = await state.name

        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"Староста {surname} {name} подал заявку на регистарцию в боте.",
                reply_markup=accept_or_deny_buttons(StudentId(student_id)),
            )
        return

    headman = await student_service.get_headman_by_group_name(await state.group_name)

    await bot.send_message(
        headman.telegram_id,
        f"Студент {student_data['surname']} {student_data['name']} подал заявку на регистарцию в вашу группу",
        reply_markup=accept_or_deny_buttons(StudentId(student_id)),
    )

    await state.clear()
