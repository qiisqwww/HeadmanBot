from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asyncpg import Pool
from loguru import logger

from src.api import ScheduleApi
from src.enums import Role
from src.handlers.command_handlers.verification_poll import verify_registration
from src.messages import (
    ASK_NAME_MESSAGE,
    ASK_SURNAME_MESSAGE,
    GROUP_DOESNT_EXISTS_MESSAGE,
    INCORRECT_STUDENT_ROLE,
    INCORRECT_UNIVERSITY,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE,
)
from src.middlewares import CheckRegistrationMiddleware
from src.reg_states import RegistrationStates
from src.registration_context import RegistrationContext

registration_router = Router()
registration_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@registration_router.message(F.text, RegistrationStates.waiting_role)
@logger.catch
async def incorrect_student_role(message: Message) -> None:
    await message.answer(INCORRECT_STUDENT_ROLE)


@registration_router.message(F.text, RegistrationStates.waiting_university)
@logger.catch
async def incorrect_university(message: Message) -> None:
    await message.answer(INCORRECT_UNIVERSITY)


@registration_router.message(F.text, RegistrationStates.waiting_group)
@logger.catch
async def handling_group(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    api = ScheduleApi(await registration_ctx.university_alias)

    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_MESSAGE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    await registration_ctx.set_group_name(message.text)
    await message.answer(ASK_SURNAME_MESSAGE)
    await registration_ctx.set_state(RegistrationStates.waiting_surname)


@registration_router.message(F.text, RegistrationStates.waiting_surname)
@logger.catch
async def handling_surname(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    await registration_ctx.set_surname(message.text)
    await message.answer(ASK_NAME_MESSAGE)
    await registration_ctx.set_state(RegistrationStates.waiting_name)


@registration_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
async def handling_name(message: Message, state: FSMContext, pool: Pool, bot: Bot) -> None:
    registration_ctx = RegistrationContext(state)

    if message.from_user is None:
        return

    if message.text is None:
        return

    await registration_ctx.set_name(message.text)
    await registration_ctx.set_telegram_id(message.from_user.id)

    await registration_ctx.set_state(RegistrationStates.on_verification)

    match registration_ctx.role:
        case Role.STUDENT:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE)
        case Role.HEADMAN:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE)

    await verify_registration(state, pool, bot)
