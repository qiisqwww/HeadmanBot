from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.headman_panel.callback_data import (
    SetViceHeadmanCallbackData,
    UnsetViceHeadmanCallbackData,
)
from src.bot.headman_panel.callback_data.choose_student_to_downgrade_callback_data import (
    ChooseStudentToDowngradeCallbackData,
)
from src.bot.headman_panel.callback_data.choose_student_to_enchance_callback_data import (
    ChooseStudentToEnhanceCallbackData,
)
from src.bot.headman_panel.callback_data import ShowStudentListCallbackData
from src.modules.student_management.domain.enums.role import Role
from src.modules.student_management.domain.models.student import Student

__all__ = [
    "group_panel_menu",
    "select_student",
]


def select_student(
    students: list[Student],
    enhance_to_vice_headman: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if enhance_to_vice_headman:
        students = list(filter(lambda s: s.role == Role.STUDENT, students))
    else:
        students = list(filter(lambda s: s.role == Role.VICE_HEADMAN, students))

    CallbackDataClass = (
        ChooseStudentToEnhanceCallbackData
        if enhance_to_vice_headman
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

    if role >= Role.HEADMAN:
        builder.button(
            text="Назначить зам. старосты",
            callback_data=SetViceHeadmanCallbackData(),
        )
        builder.button(
            text="Убрать зам. старосты",
            callback_data=UnsetViceHeadmanCallbackData(),
        )

    if role >= Role.VICE_HEADMAN:
        builder.button(
            text="Список группы",
            callback_data=ShowStudentListCallbackData(),
        )
        builder.button(
            text="Дни рождения студентов",
            callback_data=ShowStudentListCallbackData(show_birthdate=True)
        )

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
