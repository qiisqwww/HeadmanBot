import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import HEADMAN_PASSWORD
from src.messages import (
    PASS_ASK_MESSAGE,
    STAROSTA_REG_MESSAGE,
    UNSUCCESFULL_STAROSTA_REG_MESSAGE,
    WRONG_PASSWORD,
)
from src.middlewares import HeadmanRegMiddleware
from src.services import UsersService
from src.states import SetHeadman

__all__ = [
    "headman_reg_router",
]


headman_reg_router = Router()

headman_reg_router.message.middleware(HeadmanRegMiddleware())


@headman_reg_router.message(Command("set_headman"))
async def start_headmen(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=PASS_ASK_MESSAGE)
    logging.info("set_headman command, password was asked")

    await state.set_state(SetHeadman.get_password)


@headman_reg_router.message(SetHeadman.get_password, F.text)
async def get_password(message: types.Message, state: FSMContext) -> None:
    logging.info("password was handled")
    if message.text == HEADMAN_PASSWORD:
        with UsersService() as con:
            isset = con.set_status(message.from_user.id)
            if isset:
                await message.answer(text=STAROSTA_REG_MESSAGE)
            else:
                await message.answer(text=UNSUCCESFULL_STAROSTA_REG_MESSAGE)
    else:
        await message.answer(text=WRONG_PASSWORD)

    await state.clear()
