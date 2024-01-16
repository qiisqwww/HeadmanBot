from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.modules.attendance.domain import Attendance, Lesson
from src.modules.attendance.domain.enums.visit_status import VisitStatus

from ..callback_data import (
    ChooseLessonCallbackData,
    UpdateAllAttendancesCallbackData,
    UpdateAttendanceCallbackData,
)

__all__ = [
    "attendance_buttons",
    "choose_lesson_buttons",
]


def attendance_buttons(is_checked_in_today: bool, attendances: Iterable[Attendance]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for attendance in attendances:
        if is_checked_in_today:
            if attendance.status == VisitStatus.ABSENT:
                builder.button(
                    text=f"❌ Не посещу {attendance.lesson.start_time.strftime('%H:%M')} {attendance.lesson.name}",
                    callback_data=UpdateAttendanceCallbackData(
                        attendance_id=attendance.id, new_status=VisitStatus.PRESENT
                    ),
                )
            else:
                builder.button(
                    text=f"✅ Посещу {attendance.lesson.start_time.strftime('%H:%M')} {attendance.lesson.name}",
                    callback_data=UpdateAttendanceCallbackData(
                        attendance_id=attendance.id, new_status=VisitStatus.ABSENT
                    ),
                )
        else:
            builder.button(
                text=f"🤷 Неизвестно {attendance.lesson.start_time.strftime('%H:%M')} {attendance.lesson.name}",
                callback_data=UpdateAttendanceCallbackData(attendance_id=attendance.id, new_status=VisitStatus.PRESENT),
            )

    builder.button(
        text="Буду на всех",
        callback_data=UpdateAllAttendancesCallbackData(new_status=VisitStatus.PRESENT),
    )
    builder.button(
        text="Меня сегодня не будет",
        callback_data=UpdateAllAttendancesCallbackData(new_status=VisitStatus.ABSENT),
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def choose_lesson_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, lesson in enumerate(lessons):
        builder.button(
            text=f"({idx + 1}) {lesson.name} {lesson.start_time.strftime('%H:%M')}",
            callback_data=ChooseLessonCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
