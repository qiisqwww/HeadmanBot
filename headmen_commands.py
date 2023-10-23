import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from work_api import API
from service import UsersService
from buttons import load_void_kb
from messages import (load_attendance_for_headmen, NO_LESSONS_TODAY,
                      CHOOSE_GETSTAT_LESSON)
from middlewares import HeadmenCommandsMiddleware
from states import ReqPars
from aiogram.fsm.context import FSMContext


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


@router.message(Command("getstat"))
async def getstat_command(message: types.Message, state: FSMContext) -> None:
    logging.info("getstat command")

    with UsersService() as con:
        group = con.get_group_of_id_tg(message.from_user.id)
        api.regenerate(group)
        lessons = api.get_today()
        print(lessons)

        if len(lessons) == 0:
            await message.answer(NO_LESSONS_TODAY)
            return

        kb = [[types.KeyboardButton(text=f'{lesson + 1}) {lessons[lesson][0]} {lessons[lesson][1]}')]
              for lesson in range(len(lessons))]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=keyboard)

    await state.set_state(ReqPars.group_input_req)


@router.message(ReqPars.group_input_req, F.text)
async def send_attendance_msg(message: types.Message, state: FSMContext) -> None:
    logging.info("lesson name handled")

    await message.answer(text=load_attendance_for_headmen(message), reply_markup=load_void_kb())

    await state.clear()
