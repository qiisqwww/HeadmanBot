import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from work_api import API
from service import UsersService
from buttons import load_choose_lesson_kb
from messages import (NO_LESSONS_TODAY,
                      CHOOSE_GETSTAT_LESSON)
from middlewares import HeadmenCommandsMiddleware


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


@router.message(Command("getstat"))
async def getstat_command(message: types.Message) -> None:
    logging.info("getstat command")

    with UsersService() as con:
        group = con.get_group_of_id_tg(message.from_user.id)
        api.regenerate(group)
        lessons = api.get_today()

        if len(lessons) == 0:
            await message.answer(NO_LESSONS_TODAY)
            return

        await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=load_choose_lesson_kb(lessons))

