from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message
from asyncpg import Pool
from loguru import logger

from src.api import ScheduleApi
from src.enums.university_id import UniversityId
from src.messages import (
    GROUP_DOESNT_EXISTS_MESSAGE,
    REG_MESSAGE_1_1,
    REG_MESSAGE_1_2,
    REG_MESSAGE_2,
    START_MESSAGE,
    SUCCESFULLY_REG_MESSAGE,
)
from src.middlewares import CheckRegistrationMiddleware
from src.services.student_service import StudentService
from src.states import RegStates

__all__ = [
    "student_registration_router",
]

student_registration_router = Router()
student_registration_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=False))
student_registration_router.message.filter(F.chat.type.in_({"private"}))


@student_registration_router.message(Command("start"))
@logger.catch
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    logger.info("start command")

    await message.answer(f"{START_MESSAGE}\n{REG_MESSAGE_1_1}")
    await state.set_state(RegStates.surname_input)


@student_registration_router.message(RegStates.surname_input, F.text)
@logger.catch
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    logger.info("surname handled")

    await message.answer(REG_MESSAGE_1_2)
    await state.set_state(RegStates.name_input)


@student_registration_router.message(RegStates.name_input, F.text)
@logger.catch
async def handling_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    logger.info("name handled")

    await message.answer(REG_MESSAGE_2)
    await state.set_state(RegStates.group_input)


@student_registration_router.message(RegStates.group_input, F.text)
@logger.catch
async def handling_group(message: Message, state: FSMContext, pool: Pool) -> None:
    if message.from_user is None:
        return

    if message.text is None:
        await message.answer(GROUP_DOESNT_EXISTS_MESSAGE)
        return

    api = ScheduleApi(UniversityId.MIREA)
    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_MESSAGE)
        await state.set_state(RegStates.group_input)
        return

    await state.update_data(group=message.text)
    logger.info("Group name handled")

    user_data = await state.get_data()
    async with pool.acquire() as conn:
        student_service = StudentService(conn)

        await student_service.register(
            telegram_id=message.from_user.id,
            telegram_name=message.from_user.username,
            name=user_data["name"],
            surname=user_data["surname"],
            group_name=user_data["group"],
            university_id=UniversityId.MIREA,
        )
        await message.answer(SUCCESFULLY_REG_MESSAGE)

        await state.clear()
