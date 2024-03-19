from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.attendance.domain import Lesson, LessonAttendanceForGroup, VisitStatus

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

WHICH_PAIR_TEMPLATE = (
    """
Какая пара вас интересует?"""
    + "&#x200D;" * 20  # Increase message size.
)

YOU_CAN_NOT_ANSWER_TIME_TEMPLATE = """
Вы не можете отметиться! Занятия уже начались!"""

YOU_CAN_NOT_ANSWER_DAY_TEMPLATE = """
Вы не можете отметиться за другой день!"""

ALL_PAIRS_TEMPLATE = """
Вы выбрали <b>посетить все пары</b>"""

NO_PAIRS_TEMPLATE = """
Вы выбрали <b>не посещать пары</b>"""

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""

CHOOSE_PAIR_TEMPLATE = """
Выберите пару из списка:"""


def attendance_for_headmen_template(
    chosen_lesson: Lesson,
    group_attendance: LessonAttendanceForGroup,
    timezone: str,
) -> str:
    start_time = (
        convert_time_from_utc(chosen_lesson.start_time, timezone).strftime(
            "%H:%M",
        )
        + " " * 100  # Increase message size.
    )
    return render_template(
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
{% for student in group_attendance.attendance[VisitStatus.ABSENT] | sort(attribute='fullname') | selectattr('attendance_noted') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Что-то еще?""",
        lesson_name=chosen_lesson.name,
        start_time=start_time,
        group_attendance=group_attendance,
        VisitStatus=VisitStatus,
    )
