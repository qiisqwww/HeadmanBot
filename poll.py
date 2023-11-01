from aiogram import Router, F

from buttons import load_attendance_kb
from work_api import API
from service import UsersService
from middlewares import HeadmenCommandsMiddleware
from messages import POLL_MESSAGE
import logging


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
                if len(day) == 0:
                    continue
                print(day)
                first_lesson_time = day[0][1]

            except Exception as e:
                logging.warning(f"PROBLEMS IN GENERATING LESSONS (API), {e}, {group[0]}")
                continue

            con.set_time(first_lesson_time, group[0])

            for user_id in con.get_user_of_group(group[0]):
                try:
                    con.change_attendance(user_id[0], f'start {len(day)}')
                    await bot(user_id[0], POLL_MESSAGE, reply_markup=load_attendance_kb(day))
                except Exception as e:
                    logging.warning(f"PROBLEMS IN POLL, {e}")
