import logging

from aiogram import F, Router

from buttons import load_attendance_kb
from messages import POLL_MESSAGE
from middlewares import HeadmenCommandsMiddleware
from services import UsersService
from work_api import API

router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


async def job(bot):
    with UsersService() as con:
        groups = con.get_groups()
        for group in groups:
            try:
                api.regenerate(group[0])
                day = api.get_today()

            except Exception as e:
                logging.warning(f"EXCEPTION IN GENERATING LESSONS (API), {e}, {group[0]}")
                continue

            if len(day) == 0:
                continue

            first_lesson_time = day[0][1]
            con.set_time(first_lesson_time, group[0])

            for user_id in con.get_user_of_group(group[0]):
                try:
                    con.change_attendance(user_id, f"start {len(day)}")
                    await bot(user_id, POLL_MESSAGE, reply_markup=load_attendance_kb(day))
                except Exception as e:
                    logging.warning(f"EXCEPTION IN POLL, {e}")
