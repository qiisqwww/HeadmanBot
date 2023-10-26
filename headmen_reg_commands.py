import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config.config_reader import config
from service import UsersService
from states import SetHeadman
from messages import (PASS_ASK_MESSAGE, STAROSTA_REG_MESSAGE, UNSUCCESFULL_STAROSTA_REG_MESSAGE,
                      WRONG_PASSWORD)
from middlewares import HeadmenRegMiddleware

router = Router()

router.message.middleware(HeadmenRegMiddleware())

@router.message(Command("set_headmen"))
async def start_headmen(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=PASS_ASK_MESSAGE)
    logging.info("set_headmen command, password was asked")

    await state.set_state(SetHeadman.get_password)


@router.message(SetHeadman.get_password, F.text)
async def get_password(message: types.Message, state: FSMContext) -> None:
    logging.info("password was handled")
    if message.text == config.PASSWORD.get_secret_value():
        with UsersService() as con:
            isset = con.set_status(message.from_user.id)
            if isset:
                await message.answer(text=STAROSTA_REG_MESSAGE)
            else:
                await message.answer(text=UNSUCCESFULL_STAROSTA_REG_MESSAGE)
    else:
        await message.answer(text=WRONG_PASSWORD)

    await state.clear()