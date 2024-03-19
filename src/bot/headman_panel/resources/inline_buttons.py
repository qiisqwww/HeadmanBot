from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.trim_inline_text import trim_inline_text
from src.bot.headman_panel.callback_data import (
    ChooseLessonCallbackData,
    SetViceHeadmanCallbackData,
    ShowAttendanceCallbackData,
    UnsetViceHeadmanCallbackData,
)
from src.bot.headman_panel.callback_data.choose_student_to_downgrade_callback_data import (
    ChooseStudentToDowngradeCallbackData,
)
from src.bot.headman_panel.callback_data.choose_student_to_enchance_callback_data import (
    ChooseStudentToEnhanceCallbackData,
)
from src.modules.attendance.domain import Lesson
from src.modules.student_management.domain.enums.role import Role
from src.modules.student_management.domain.models.student_info import StudentInfo

__all__ = [
    "group_panel_menu",
]


def select_student(
    students: list[StudentInfo],
    enchance_to_vice_headman: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    CallbackDataClass = (
        ChooseStudentToEnhanceCallbackData
        if enchance_to_vice_headman
        else ChooseStudentToDowngradeCallbackData
    )

    students.sort(key=lambda s: s.fullname)

    for student in students:
        builder.button(
            text=f"{student.last_name} {student.first_name}",
            callback_data=CallbackDataClass(
                student_id=student.id,
                telegram_id=student.telegram_id,
            ),
        )

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def group_panel_menu(role: Role) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Узнать посещаемость",
        callback_data=ShowAttendanceCallbackData(),
    )

    if role >= Role.HEADMAN:
        builder.button(
            text="Назначить зама старосты",
            callback_data=SetViceHeadmanCallbackData(),
        )
        builder.button(
            text="Убрать зама старосты",
            callback_data=UnsetViceHeadmanCallbackData(),
        )

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


__all__ = [
    "choose_lesson_buttons",
]


def choose_lesson_buttons(
    lessons: Iterable[Lesson],
    student_timezone: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for lesson in lessons:
        start_time = convert_time_from_utc(lesson.start_time, student_timezone)
        button_text = trim_inline_text(f"{start_time:%H:%M} {lesson.name}")
        builder.button(
            text=button_text,
            callback_data=ChooseLessonCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
