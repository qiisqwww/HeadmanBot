import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from service import UsersService
from states import RegStates
from messages import (START_MESSAGE, REG_MESSAGE_1_1, REG_MESSAGE_1_2, REG_MESSAGE_2,
                      SUCCESFULLY_REG_MESSAGE, UNSUCCESFULLY_REG_MESSAGE)
from middlewares import RegMiddleware
from work_api import API
router = Router()

router.message.middleware(RegMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext) -> None:
    logging.info("start command")

    await message.answer(text=START_MESSAGE + '\n' + REG_MESSAGE_1_1)
    await state.set_state(RegStates.surname_input)


@router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    logging.info("surname handled")

    await message.answer(text = REG_MESSAGE_1_2)
    await state.set_state(RegStates.name_input)


@router.message(RegStates.name_input, F.text)
async def handling_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    logging.info("name handled")

    await message.answer(text=REG_MESSAGE_2)
    await state.set_state(RegStates.group_input)


@router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    api = API()
    if not api.regenerate(message.text)[0]:
        await message.answer(text="Такой группы нет!")
        await state.set_state(RegStates.group_input)
        return

    await state.update_data(group=message.text)
    logging.info("group name handled")

    user_data = await state.get_data()

    with UsersService() as con:
        isreg: bool = con.registration(message.from_user.id, message.from_user.username,
                                       user_data["surname"] + " " + user_data["name"], user_data["group"])

        if isreg:
            await message.answer(text=SUCCESFULLY_REG_MESSAGE)
        else:
            await message.answer(text=UNSUCCESFULLY_REG_MESSAGE)

    await state.clear()
