import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config.config_reader import config

from service import UsersService
from states import RegStates, SetHeadMen
from messages import (START_MESSAGE, REG_MESSAGE_1, REG_MESSAGE_2,
                      SUCCESFULLY_REG_MESSAGE, UNSUCCESFULLY_REG_MESSAGE, PASS_ASK_MESSAGE,
                      STAROSTA_REG_MESSAGE, UNSUCCESFULL_STAROSTA_REG_MESSAGE)
from middlewares import RegMiddleware

router = Router()

router.message.middleware(RegMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

@router.message(Command("start"))
async def start_cmd(message: types.Message, state:FSMContext) -> None:
    await message.answer(text = START_MESSAGE + '\n'+ REG_MESSAGE_1)
    logging.info("start command")

    await state.set_state(RegStates.surname_input)

@router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name_surname = message.text)
    logging.info("name and surname handled")

    await message.answer(text = REG_MESSAGE_2)

    await state.set_state(RegStates.group_input)

@router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    await state.update_data(group = message.text)
    logging.info("group name handled")

    user_data = await state.get_data()

    with UsersService() as con:
        isreg : bool = con.registration(message.from_user.id,message.from_user.username,user_data["name_surname"],
                                        user_data["group"])
        if isreg: await message.answer(text = SUCCESFULLY_REG_MESSAGE)
        else: await message.answer(text = UNSUCCESFULLY_REG_MESSAGE)

        await state.clear()

@router.message(Command("set_headmen"))
async def start_headmen(message: types.Message, state:FSMContext) -> None:
    await message.answer(text = PASS_ASK_MESSAGE)

    await state.set_state(RegStates.surname_input)

@router.message(SetHeadMen.get_password, F.text)
async def get_password(message: types.Message, state:FSMContext) -> None:
    if message.text == config.PASSWORD.get_secret_value():
        with UsersService() as con:
            isset = con.set_headmen()
            if isset: await message.answer(text = STAROSTA_REG_MESSAGE)
            else: await message.answer(text = UNSUCCESFULL_STAROSTA_REG_MESSAGE)

    await state.clear()

