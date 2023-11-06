import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.messages import (
    GROUP_DOESNT_EXISTS_MESSAGE,
    REG_MESSAGE_1_1,
    REG_MESSAGE_1_2,
    REG_MESSAGE_2,
    START_MESSAGE,
    SUCCESFULLY_REG_MESSAGE,
)
from src.middlewares import RegMiddleware
from src.mirea_api import MireaScheduleApi
from src.services.student_service import StudentService
from src.states import RegStates

__all__ = [
    "personal_chat_router",
]


personal_chat_router = Router()

personal_chat_router.message.middleware(RegMiddleware())
personal_chat_router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@personal_chat_router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    logging.info("start command")

    await message.answer(f"{START_MESSAGE}\n{REG_MESSAGE_1_1}")
    await state.set_state(RegStates.surname_input)


@personal_chat_router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    logging.info("surname handled")

    await message.answer(REG_MESSAGE_1_2)
    await state.set_state(RegStates.name_input)


@personal_chat_router.message(RegStates.name_input, F.text)
async def handling_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    logging.info("name handled")

    await message.answer(REG_MESSAGE_2)
    await state.set_state(RegStates.group_input)


@personal_chat_router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    api = MireaScheduleApi()
    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_MESSAGE)
        await state.set_state(RegStates.group_input)
        return

    await state.update_data(group=message.text)
    logging.info("group name handled")

    user_data = await state.get_data()

    async with StudentService() as student_service:
        await student_service.create(
            telegram_id=message.from_user.id,
            telegram_name=message.from_user.username,
            name=user_data["name"],
            surname=user_data["surname"],
            group_name=user_data["group"],
        )
        await message.answer(SUCCESFULLY_REG_MESSAGE)

    await state.clear()
