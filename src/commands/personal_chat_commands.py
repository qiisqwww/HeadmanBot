import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from messages import (
    REG_MESSAGE_1_1,
    REG_MESSAGE_1_2,
    REG_MESSAGE_2,
    START_MESSAGE,
    SUCCESFULLY_REG_MESSAGE,
    UNSUCCESFULLY_REG_MESSAGE,
)
from middlewares import RegMiddleware
from services import UsersService
from states import RegStates
from work_api import API

__all__ = [
    "personal_chat_router",
]


personal_chat_router = Router()

personal_chat_router.message.middleware(RegMiddleware())
personal_chat_router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@personal_chat_router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    logging.info("start command")

    await message.answer(text=START_MESSAGE + "\n" + REG_MESSAGE_1_1)
    await state.set_state(RegStates.surname_input)


@personal_chat_router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    logging.info("surname handled")

    await message.answer(text=REG_MESSAGE_1_2)
    await state.set_state(RegStates.name_input)


@personal_chat_router.message(RegStates.name_input, F.text)
async def handling_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    logging.info("name handled")

    await message.answer(text=REG_MESSAGE_2)
    await state.set_state(RegStates.group_input)


@personal_chat_router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    api = API()
    if not api.regenerate(message.text):
        await message.answer(text="Такой группы нет!")
        await state.set_state(RegStates.group_input)
        return

    await state.update_data(group=message.text)
    logging.info("group name handled")

    user_data = await state.get_data()

    with UsersService() as con:
        isreg: bool = con.registration(
            message.from_user.id,
            message.from_user.username,
            user_data["surname"] + " " + user_data["name"],
            user_data["group"],
        )

        if isreg:
            await message.answer(text=SUCCESFULLY_REG_MESSAGE)
        else:
            await message.answer(text=UNSUCCESFULLY_REG_MESSAGE)

    await state.clear()
