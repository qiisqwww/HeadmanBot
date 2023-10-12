#import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from service import UsersService
from states import RegStates
from messages import (START_MESSAGE, REG_MESSAGE_0,REG_MESSAGE_1, REG_MESSAGE_2,
                      SUCCESFULLY_REG_MESSAGE, UNSUCCESFULLY_REG_MESSAGE)

router = Router()

router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

@router.message(Command("start"))
async def start_cmd(message: types.Message, state:FSMContext) -> None:
    await message.answer(text = START_MESSAGE + '\n'+ REG_MESSAGE_1)

    await state.set_state(RegStates.surname_input)

@router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname = message.text)

    await message.answer(text = REG_MESSAGE_2)

    await state.set_state(RegStates.group_input)

@router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    await state.update_data(group = message.text)

    user_data = await state.get_data()

    with UsersService() as con:
        isreg : bool = con.registration(message.from_user.id,message.from_user.username,user_data["surname"],
                                        user_data["group"])
        if isreg: await message.answer(text = SUCCESFULLY_REG_MESSAGE)
        else: await message.answer(text = UNSUCCESFULLY_REG_MESSAGE)

        await state.clear()



