from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template

from src.dto.entities import Student, Attendance
from src.dto.enums import VisitStatus

__all__ = [
    "POLL_TEMPLATE",
    "your_all_choice_is_template",
    "your_choice_is_template",
    "student_was_not_polled_warning_template",
]

POLL_TEMPLATE = "На какие сегодняшие пары ты придешь?"


def your_all_choice_is_template(status: VisitStatus) -> str:
    match status:
        case VisitStatus.PRESENT:
            return "Вы выбрали <b>посетить все пары</b>. Отличный выбор."
        case VisitStatus.ABSENT:
            return "Вы выбрали <b>не посещать пары</b>. Ничего страшного, придете в следующий раз."


def your_choice_is_template(attendance: Attendance, timezone: str) -> str:
    start_time = convert_time_from_utc(attendance.lesson.start_time, timezone).strftime(
        "%H:%M",
    )
    template = """
Вы выбрали{% if attendance.status == 'PRESENT' %} посетить {% else %} не посещать {% endif %}
<b>{{attendance.lesson.name}} {{start_time}}</b>"""
    return render_template(
        template,
        attendance=attendance,
        start_time=start_time,
    )


def student_was_not_polled_warning_template(student: Student) -> str:
    template = """
Студент <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a> не получил рассылку,
так как заблокировал бота."""
    return render_template(template, student=student)
