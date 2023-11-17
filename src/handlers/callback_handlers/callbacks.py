from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery
from asyncpg import Pool
from loguru import logger

from src.resources import (load_attendance_buttons,
                           load_choose_lesson_buttons,
                           load_void_button)
from src.dto.student import Student
from src.enums import VisitStatus
from src.resources import (ALL_MESSAGE,
                           NONE_MESSAGE,
                           attendance_for_headmen_message)
from src.middlewares import CheckRegistrationMiddleware
from src.services import AttendanceService
from src.services.lesson_service import LessonService

__all__ = [
    "callback_router",
]


callback_router = Router()
callback_router.callback_query.middleware(CheckRegistrationMiddleware(must_be_registered=True))


@callback_router.callback_query(F.data.startswith("attendance"),
                                flags={"callback": "poll"})
@logger.catch
async def check_in_callback(callback: CallbackQuery, pool: Pool, student: Student):
    if callback.message is None:
        return

    if callback.data is None:
        logger.error("No callback data for change attendance.")
        return

    callback_data = callback.data.split("_")[1]

    async with pool.acquire() as con:
        attendance_service = AttendanceService(con)

        if callback_data == "all":
            await attendance_service.update_visit_status_by_student(student, VisitStatus.VISIT)
            await callback.message.edit_text(ALL_MESSAGE, reply_markup=load_void_button())
            return

        if callback_data == "none":
            await attendance_service.update_visit_status_by_student(student, VisitStatus.NOT_VISIT)
            await callback.message.edit_text(NONE_MESSAGE, reply_markup=load_void_button())
            return

        choosen_lesson_id = int(callback_data)

        await attendance_service.update_visit_status(student, choosen_lesson_id, VisitStatus.VISIT)
        attendances = await attendance_service.filter_by_student(student)

        choosen_lesson = next(filter(lambda attendance: attendance.lesson.id == choosen_lesson_id, attendances)).lesson
        non_visit_lessons = [attendance.lesson for attendance in attendances if attendance.status != VisitStatus.VISIT]

        if non_visit_lessons:
            keyboard = load_attendance_buttons(non_visit_lessons)
            text = f"Вы посетите пару {choosen_lesson.name}, которая начнётся в {choosen_lesson.str_start_time}"
        else:
            keyboard = load_void_button()
            text = ALL_MESSAGE

        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
        )


@callback_router.callback_query(flags={"callback": "attendance"})
@logger.catch
async def attendance_send_callback(callback: CallbackQuery, pool: Pool, student: Student):
    if callback.message is None:
        return

    if callback.data is None:
        return

    logger.info("attendance callback handled")

    choosen_lesson_id = int(callback.data)

    async with pool.acquire() as con:
        lesson_service = LessonService(con)

        lessons = await lesson_service.filter_by_student(student)
        choosen_lesson = next(filter(lambda lesson: lesson.id == choosen_lesson_id, lessons))

        attendance_list_msg = await attendance_for_headmen_message(choosen_lesson, student, con)
        await callback.message.edit_text(
            text=f"{choosen_lesson}\n\n{attendance_list_msg}",
            reply_markup=load_choose_lesson_buttons(lessons),
        )
