from jinja2 import Template

from src.modules.attendance.domain import Lesson, LessonAttendanceForGroup

__all__ = [
    "ALL_PAIRS_TEMPLATE",
    "NO_PAIRS_TEMPLATE",
    "NO_LESSONS_TODAY_TEMPLATE",
    "CHOOSE_PAIR_TEMPLATE",
    "POLL_TEMPLATE",
    "WHICH_PAIR_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_TIME_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_DAY_TEMPLATE",
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

POLL_TEMPLATE = """
На какие сегодняшие пары ты придешь?

Если возникли проблемы - напишите о них в @noheadproblemsbot"""


def attendance_for_headmen_template(choosen_lesson: Lesson, group_attendance: LessonAttendanceForGroup) -> str:
    template = Template(
        """{{lesson.name}} {{lesson.start_time.strftime('%H:%M')}}

Не отметились:
{% for student in group_attendance.attendance['absent'] -%}
    {% if not student.is_checked_in_today -%}
        <a href="tg://user?id={{ student.telegram_id }}">{{ student.surname }} {{ student.name }}</a>
    {%- endif %}
{%- endfor %}

Придут:
{% for student in group_attendance.attendance['present'] -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.surname }} {{ student.name }}</a>
{%- endfor %}

Не придут:
{% for student in group_attendance.attendance['absent'] -%}
    {% if student.is_checked_in_today -%}
        <a href="tg://user?id={{ student.telegram_id }}">{{ student.surname }} {{ student.name }}</a>
    {%- endif %}
{%- endfor %}

Что-то еще?""",
        autoescape=True,
    )

    return template.render(lesson=choosen_lesson, group_attendance=group_attendance)
