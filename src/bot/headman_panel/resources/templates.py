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
    "YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE",
    "STUDENT_WAS_NOT_FOUND_TEMPLATE",
    "YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE",
    "FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE",
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

YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE = """Вы были повышены до заместителя старосты.
Вы теперь можете просматривать посещаемость группы. Для просмотра посещаемости нажмите на кнопку "Группа".
"""

YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE = "С вас была снята роль заместителя старосты."

STUDENT_WAS_NOT_FOUND_TEMPLATE = "Пользователь не был найден, попробуйте заново."

FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE = (
    'Можно дать роль заместителя старосты только пользователю с ролью "студент".'
)

FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE = (
    'Можно снять роль заместителя старосты только пользователю с ролью "зам старосты".'
)


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
