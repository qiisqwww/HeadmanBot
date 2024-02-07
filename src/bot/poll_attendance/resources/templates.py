from jinja2 import Template

from src.modules.attendance.domain import Attendance, VisitStatus, StudentInfo

__all__ = [
    "POLL_TEMPLATE",
    "your_all_choice_is_template",
    "your_choice_is_template",
    "student_was_not_polled_warning_template"
]


POLL_TEMPLATE = "На какие сегодняшие пары ты придешь?"


def your_all_choice_is_template(status: VisitStatus) -> str:
    match status:
        case VisitStatus.PRESENT:
            return "Вы выбрали <b>посетить все пары</b>. Отличный выбор."
        case VisitStatus.ABSENT:
            return "Вы выбрали <b>не посещать пары</b>. Ничего страшного, прийдете в следующий раз."


def your_choice_is_template(attendance: Attendance) -> str:
    template: str = Template(
        "Вы выбрали{% if attendance.status == 'present' %} посетить {% else %} не посещать {% endif %}"
        "<b>{{attendance.lesson.name}} {{attendance.lesson.start_time.strftime('%H:%M')}}</b>",
        autoescape=True,
    ).render(attendance=attendance)

    return template


def student_was_not_polled_warning_template(student_info: StudentInfo) -> str:
    template: str = Template(
        'Студент <a href="tg://user?id={{ student_info.telegram_id }}">{{ student_info.surname }} '
        '{{ student_info.name }}</a> не получил рассылку, так как заблокировал бота.',
        autoescape=True
    ).render(student_info=student_info)

    return template
