from datetime import date

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asyncpg import Pool
from loguru import logger

from src.api.schedule_api import ScheduleApi
from src.auth.handlers.registration_context import RegistrationContext
from src.auth.handlers.registration_states import RegistrationStates
from src.auth.handlers.validation import is_number
from src.auth.resources.inline_buttons import accept_or_deny_buttons
from src.auth.resources.templates import (
    ASK_BIRTHDAY_TEMPLATE,
    ASK_BIRTHMONTH_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    BIRTHDAY_INCORRECT_TEMPLATE,
    BIRTHDAY_MUST_BE_DIGIT_TEMPLATE,
    BIRTHMONTH_INCORRECT_TEMPLATE,
    BIRTHMONTH_MUST_BE_DIGIT_TEMPLATE,
    GROUP_ALREADY_EXISTS_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
)
from src.auth.services import CacheStudentService
from src.bot import AuthContractService
from src.config import ADMIN_IDS
from src.enums import Role
from src.middlewares import CheckRegistrationMiddleware

__all__ = [
    "registration_finite_state_router",
]

registration_finite_state_router = Router()
registration_finite_state_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=False))


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
async def handling_group(message: Message, state: FSMContext, pool: Pool) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    api = ScheduleApi(await registration_ctx.university_alias)

    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    async with pool.acquire() as con:
        auth_contract_service = AuthContractService(con)
        group = await auth_contract_service.find_group_by_name_and_uni(
            message.text, await registration_ctx.university_alias
        )

    if await registration_ctx.role == Role.HEADMAN and group is not None:
        await message.answer(GROUP_ALREADY_EXISTS_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    await registration_ctx.set_group_name(message.text)
    await message.answer(ASK_BIRTHMONTH_TEMPLATE)
    await registration_ctx.set_state(RegistrationStates.waiting_birthmonth)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthmonth)
@logger.catch
async def handling_birthmonth(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    if not is_number(message.text):
        await message.answer(BIRTHMONTH_MUST_BE_DIGIT_TEMPLATE)
        return

    birthmonth = int(message.text)

    if 1 <= birthmonth <= 12:
        await registration_ctx.set_birthmonth(birthmonth)
        await message.answer(ASK_BIRTHDAY_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_birthday)
    elif birthmonth == 0:
        await registration_ctx.set_birthmonth(0)
        await registration_ctx.set_birthday(0)
        await registration_ctx.set_state(RegistrationStates.waiting_surname)
        await message.answer(ASK_SURNAME_TEMPLATE)
    else:
        await message.answer(BIRTHMONTH_INCORRECT_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_birthmonth)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthday)
@logger.catch
async def handling_birthday(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    if not is_number(message.text):
        await message.answer(BIRTHDAY_MUST_BE_DIGIT_TEMPLATE)
        return

    birthday = int(message.text)

    try:
        date(year=2023, month=await registration_ctx.birthmonth, day=birthday)
    except ValueError:
        await message.answer(BIRTHDAY_INCORRECT_TEMPLATE)
        return

    await registration_ctx.set_birthday(birthday)
    await registration_ctx.set_state(RegistrationStates.waiting_surname)
    await message.answer(ASK_SURNAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_surname)
@logger.catch
async def handling_surname(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    await registration_ctx.set_surname(message.text)
    await registration_ctx.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
async def handling_name(message: Message, state: FSMContext, bot: Bot) -> None:
    registration_ctx = RegistrationContext(state)

    if message.from_user is None:
        return

    if message.text is None:
        return

    await registration_ctx.set_name(message.text)
    await registration_ctx.set_telegram_id(message.from_user.id)
    await registration_ctx.set_state(RegistrationStates.on_verification)

    match await registration_ctx.role:
        case Role.STUDENT:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    student_data = await registration_ctx.get_data()
    async with CacheStudentService() as cache_student_service:
        await cache_student_service.cache_student(student_data)

    if await registration_ctx.role == Role.HEADMAN:
        surname = await registration_ctx.surname
        name = await registration_ctx.name
        student_id = await registration_ctx.telegram_id

        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"Староста {surname} {name} подал заявку на регистарцию в боте.",
                reply_markup=accept_or_deny_buttons(student_id),
            )
        return

    # async with pool.acquire() as con:
    #     group_service = GroupService(con)
    #     group = await group_service.get_by_name(user_data["group_name"])
    #
    #     students_service = StudentService(con)
    #     students = await students_service.filter_by_group(group)
    #
    # headmans = [student for student in students if student.is_headman]
    #
    # for headman in headmans:
    #     await bot.send_message(
    #         headman.telegram_id,
    #         f"Студент {user_data['surname']} {user_data['name']} подал заявку на регистарцию в вашу группу",
    #         reply_markup=accept_or_deny_buttons(user_id),
    #     )

    await state.clear()
