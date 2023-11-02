import logging

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from buttons import load_choose_lesson_kb
from messages import (
    CHOOSE_GETSTAT_LESSON,
    FAQ_MESSAGE,
    HEADMAN_SEND_MSG_MISTAKE,
    NO_LESSONS_TODAY,
)
from middlewares import HeadmenCommandsMiddleware
from services import UsersService
from work_api import API

__all__ = ["router"]


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


@router.message(Command("getstat"))
async def getstat_command(message: types.Message) -> None:
    logging.info("getstat command")

    with UsersService() as con:
        group = con.get_group_of_id_tg(message.from_user.id)
        if not api.regenerate(group):
            await message.answer(HEADMAN_SEND_MSG_MISTAKE)
            return
        lessons = api.get_today()

        if len(lessons) == 0:
            await message.answer(NO_LESSONS_TODAY)
            return

        await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=load_choose_lesson_kb(lessons))


@router.message(Command("faq"))
async def faq_command(message: types.Message) -> None:
    logging.info("faq command")

    await message.answer(FAQ_MESSAGE, parse_mode=ParseMode.MARKDOWN)
