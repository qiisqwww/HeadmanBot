from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.attendance.domain import Attendance, VisitStatus
from src.modules.student_management.domain import StudentInfo

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
            return "Вы выбрали <b>не посещать пары</b>. Ничего страшного, прийдете в следующий раз."


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


def student_was_not_polled_warning_template(student_info: StudentInfo) -> str:
    template = """
Студент <a href="tg://user?id={{ student_info.telegram_id }}">{{ student_info.fullname }}</a> не получил рассылку,
так как заблокировал бота."""
    return render_template(template, student_info=student_info)
