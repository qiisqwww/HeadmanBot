from jinja2 import Template

from src.bot.common.convert_time import convert_time_from_utc
from src.modules.attendance.domain import Attendance, StudentInfo, VisitStatus

__all__ = [
    "POLL_TEMPLATE",
    "YOU_MUST_REMEMBER_TEMPLATE",
    "your_all_choice_is_template",
    "your_choice_is_template",
    "student_was_not_polled_warning_template",
]


POLL_TEMPLATE = "На какие сегодняшие пары ты придешь?"

YOU_MUST_REMEMBER_TEMPLATE = """
Помни, что только ты <i>сам</i> решаешь, отмечаться в боте честно или обманывать своего старосту. Однако ты должен понимать,
что в таком случае подставляешь его, потому призываем не злоупотреблять доверием старосты и указывать только правду.
"""


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


def student_was_not_polled_warning_template(student_info: StudentInfo) -> str:
    template: str = Template(
        'Студент <a href="tg://user?id={{ student_info.telegram_id }}">{{ student_info.last_name }} '
        '{{ student_info.first_name }}</a> не получил рассылку, так как заблокировал бота.',
        autoescape=True,
    ).render(student_info=student_info)

    return template
