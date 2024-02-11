from jinja2 import Template

from src.bot.common.convert_time import convert_time_from_utc
from src.modules.attendance.domain import (
    Lesson,
    LessonAttendanceForGroup,
)
from src.modules.attendance.domain.enums.visit_status import VisitStatus

__all__ = [
    "ALL_PAIRS_TEMPLATE",
    "NO_PAIRS_TEMPLATE",
    "NO_LESSONS_TODAY_TEMPLATE",
    "CHOOSE_PAIR_TEMPLATE",
    "WHICH_PAIR_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_TIME_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_DAY_TEMPLATE",
    "attendance_for_headmen_template",
]

WHICH_PAIR_TEMPLATE = """
Какая пара вас интересует?"""

YOU_CAN_NOT_ANSWER_TIME_TEMPLATE = """
Вы не можете отметиться! Занятия уже начались!"""

YOU_CAN_NOT_ANSWER_DAY_TEMPLATE = """
Вы не можете отметиться за другой день!"""

ALL_PAIRS_TEMPLATE = """
Вы посетите все пары"""

NO_PAIRS_TEMPLATE = """
Вы не посетите пары """

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""

CHOOSE_PAIR_TEMPLATE = """
Выберите пару из списка:"""


def attendance_for_headmen_template(choosen_lesson: Lesson, group_attendance: LessonAttendanceForGroup, timezone: str) -> str:
    start_time = convert_time_from_utc(choosen_lesson.start_time, timezone).strftime("%H:%M")
    template: str = Template(
        """{{lesson_name}} {{start_time}}

Не отметились:
{% for student in group_attendance.attendance[VisitStatus.ABSENT] | sort(attribute='fullname') | rejectattr('attendance_noted') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Придут:
{% for student in group_attendance.attendance[VisitStatus.PRESENT] | sort(attribute='fullname') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Не придут:
{% for student in group_attendance.attendance[VisitStatus.ABSENT] | sort(attribute='fullname') | rejectattr('attendance_noted', '==', False) -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Что-то еще?""",
        autoescape=True,trim_blocks=True,
    ).render(lesson_name=choosen_lesson.name, start_time=start_time, group_attendance=group_attendance,VisitStatus=VisitStatus)

    return template
