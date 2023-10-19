import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from service import UsersService
"""нужно заимпортить из messages сообщение, которое будет выводиться в getstat_command
!!! - сообщение еще не создано, оно должно содержать результат ответа юзеров группы старосты"""
from middlewares import HeadmenCommandsMiddleware

router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@router.message(Command("getstat"))
async def getstat_command(message: types.Message):
    logging.info("getstat command")
    # команда не готова, необходимо доделать сообщение