import logging

from aiogram import F, Router

from .buttons import load_attendance_kb
from .messages import POLL_MESSAGE
from .middlewares import HeadmenCommandsMiddleware
from .mirea_api import MireaScheduleApi
from .services import UsersService

router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = MireaScheduleApi()


async def job(bot):
    with UsersService() as con:
        groups = con.get_groups()
        for group in groups:
            try:
                lessons = await api.get_schedule(group[0])

            except Exception as e:
                logging.warning(f"EXCEPTION IN GENERATING LESSONS (API), {e}, {group[0]}")
                continue

            if not lessons:
                continue

            first_lesson_time = lessons[0].start_time
            con.set_time(first_lesson_time, group[0])

            for user_id in con.get_user_of_group(group[0]):
                try:
                    con.change_attendance(user_id, f"start {len(lessons)}")
                    await bot(user_id, POLL_MESSAGE, reply_markup=load_attendance_kb(lessons))
                except Exception as e:
                    logging.warning(f"EXCEPTION IN POLL, {e}")
