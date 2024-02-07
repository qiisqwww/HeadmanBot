from jinja2 import Template

from src.bot.common.convert_time import convert_time_from_utc
from src.modules.attendance.domain import Attendance, VisitStatus

__all__ = [
    "POLL_TEMPLATE",
    "your_all_choice_is_template",
    "your_choice_is_template",
]



POLL_TEMPLATE = "На какие сегодняшие пары ты придешь?"

def your_all_choice_is_template(status: VisitStatus) -> str:
    match status:
        case VisitStatus.PRESENT:
            return "Вы выбрали <b>посетить все пары</b>. Отличный выбор."
        case VisitStatus.ABSENT:
            return "Вы выбрали <b>не посещать пары</b>. Ничего страшного, прийдете в следующий раз."


def your_choice_is_template(attendance: Attendance, timezone: str) -> str:
    start_time = convert_time_from_utc(attendance.lesson.start_time, timezone)
    template: str = Template(
        "Вы выбрали{% if attendance.status == 'present' %} посетить {% else %} не посещать {% endif %}"
        "<b>{{attendance.lesson.name}} {{start_time.strftime('%H:%M')}}</b>",
        autoescape=True,
    ).render(attendance=attendance, start_time=start_time)

    return template
