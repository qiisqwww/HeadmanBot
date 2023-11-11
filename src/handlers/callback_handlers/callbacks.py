from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types.callback_query import CallbackQuery
from asyncpg import Pool
from loguru import logger

from src.buttons import load_attendance_kb, load_choose_lesson_kb, load_void_kb
from src.enums import VisitStatus
from src.messages import ALL_MESSAGE, NONE_MESSAGE, attendance_for_headmen_message
from src.middlewares import CheckRegistrationMiddleware
from src.services import AttendanceService, LessonService, StudentService

__all__ = [
    "callback_router",
]


callback_router = Router()
callback_router.callback_query.middleware(CheckRegistrationMiddleware(must_be_registered=True))


@callback_router.callback_query(F.data.startswith("attendance"), flags={"callback": "poll"})
@logger.catch
async def check_in_callback(callback: CallbackQuery, pool: Pool):
    if callback.message is None:
        return

    if callback.data is None:
        logger.error("No callback data for change attendance.")
        return

    callback_data = callback.data.split("_")[1]
    user_id = callback.from_user.id

    async with pool.acquire() as conn:
        attendance_service = AttendanceService(conn)
        lesson_service = LessonService(conn)

        if callback_data == "all":
            await attendance_service.set_status_for_all_lessons(user_id, VisitStatus.VISIT)
            await callback.message.edit_text(ALL_MESSAGE, reply_markup=load_void_kb())
            return

        if callback_data == "none":
            await attendance_service.set_status_for_all_lessons(user_id, VisitStatus.NOT_VISIT)
            await callback.message.edit_text(NONE_MESSAGE, reply_markup=load_void_kb())
            return

        choosen_lesson = await lesson_service.get(int(callback_data))
        attendance = await attendance_service.get(user_id)

        await attendance_service.set_status(user_id, choosen_lesson.id, VisitStatus.VISIT)

        for lesson, status in attendance.lessons:
            if status == VisitStatus.NOT_CHECKED:
                await attendance_service.set_status(user_id, lesson.id, VisitStatus.NOT_VISIT)

        non_visit_lessons = list(filter(lambda el: el[1] != VisitStatus.VISIT, attendance.lessons))

        await callback.message.edit_text(
            f"Вы посетите пару {choosen_lesson.discipline}, которая начнётся в {choosen_lesson.start_time.strftime('%H:%M')}",
            reply_markup=load_attendance_kb([lesson for lesson, _ in non_visit_lessons]),
        )


@callback_router.callback_query(flags={"callback": "attendance"})
@logger.catch
async def attendance_send_callback(callback: CallbackQuery, pool: Pool):
    if callback.message is None:
        return

    logger.info("attendance callback handled")

    headman_id = callback.from_user.id
    lesson_id = int(callback.data)

    async with pool.acquire() as conn:
        student_service = StudentService(conn)

        schedule = await student_service.get_schedule(headman_id)
        lesson = tuple(filter(lambda lesson: lesson.id == lesson_id, schedule))[0]

        await callback.message.edit_text(
            text=f"{lesson.discipline}, {lesson.start_time.strftime('%H:%M')}\n\n"
            + await attendance_for_headmen_message(lesson_id, headman_id, conn),
            reply_markup=load_choose_lesson_kb(schedule),
            parse_mode=ParseMode.HTML,
        )
