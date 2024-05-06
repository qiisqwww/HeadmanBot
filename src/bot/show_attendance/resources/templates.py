from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.attendance.domain.enums.visit_status import VisitStatus
from src.modules.attendance.domain.models.lesson import Lesson
from src.modules.attendance.domain.models.lesson_attendance_for_group import (
    LessonAttendanceForGroup,
)

__all__ = [
    "CHOOSE_PAIR_TEMPLATE",
    "NO_LESSONS_TODAY_TEMPLATE",
    "WHICH_PAIR_TEMPLATE",
    "attendance_for_headmen_template",
]

CHOOSE_PAIR_TEMPLATE = """
Выберите пару из списка:"""

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""

WHICH_PAIR_TEMPLATE = (
    """
Какая пара вас интересует?"""
    + "&#x200D;" * 20  # Increase message size.
)


def attendance_for_headmen_template(
    chosen_lesson: Lesson,
    group_attendance: LessonAttendanceForGroup,
    timezone: str,
) -> str:
    not_checked_students = tuple(
        filter(
            lambda s: not s.attendance_noted,
            group_attendance.attendance[VisitStatus.ABSENT],
        ),
    )

    will_arrive_students = group_attendance.attendance[VisitStatus.PRESENT]

    will_not_arrive_students = tuple(
        filter(
            lambda s: s.attendance_noted,
            group_attendance.attendance[VisitStatus.ABSENT],
        ),
    )

    all_students_count = len(group_attendance.attendance[VisitStatus.ABSENT]) + len(
        group_attendance.attendance[VisitStatus.PRESENT],
    )

    start_time = (
        convert_time_from_utc(chosen_lesson.start_time, timezone).strftime(
            "%H:%M",
        )
        + " " * 100  # Increase message size.
    )
    return render_template(
        """{{lesson_name}} {{start_time}}

Не отметились <b>({{ not_checked_students|length }}/{{ all_students_count }})</b>:
{% for student in not_checked_students | sort(attribute='fullname') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Придут <b>({{ will_arrive_students|length }}/{{ all_students_count }})</b>:
{% for student in will_arrive_students | sort(attribute='fullname') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Не придут <b>({{ will_not_arrive_students|length }}/{{ all_students_count }})</b>:
{% for student in will_not_arrive_students | sort(attribute='fullname') -%}
    <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}

Что-то еще?""",
        lesson_name=chosen_lesson.name,
        start_time=start_time,
        all_students_count=all_students_count,
        not_checked_students=not_checked_students,
        will_arrive_students=will_arrive_students,
        will_not_arrive_students=will_not_arrive_students,
    )
