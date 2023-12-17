from src.dto.models import StudentReadFullname
from src.enums import VisitStatus

__all__ = [
    "ALL_MESSAGE",
    "NONE_MESSAGE",
    "NO_LESSONS_TODAY",
    "CHOOSE_PAIR_MESSAGE",
    "POLL_MESSAGE",
    "WHICH_PAIR_MESSAGE",
    "attendance_for_headmen_message",
]


WHICH_PAIR_MESSAGE = """
Какая пара вас интересует?"""


ALL_MESSAGE = """
Вы посетите все пары"""

NONE_MESSAGE = """
Вы не посетите пары """

NO_LESSONS_TODAY = """
Сегодня нет пар!"""

CHOOSE_PAIR_MESSAGE = """
Выберите пару из списка:"""

POLL_MESSAGE = """
На какие сегодняшие пары ты придешь?

Если возникли проблемы - напишите о них в @noheadproblemsbot"""


def telegram_link_template(student_meta: StudentReadFullname) -> str:
    return f'<a href="tg://user?id={student_meta.telegram_id}">{student_meta.surname} {student_meta.name}</a>\n'


def attendance_for_headmen_message(group_attendance: dict[StudentReadFullname, VisitStatus]) -> str:
    visit_text = "Придут:\n"
    none_text = "Не отметились:\n"
    no_text = "Не придут:\n"

    not_visit: list[StudentReadFullname] = []
    visit: list[StudentReadFullname] = []
    not_checked: list[StudentReadFullname] = []

    for student, visit_status in group_attendance.items():
        match visit_status:
            case VisitStatus.NOT_CHECKED:
                not_checked.append(student)
            case VisitStatus.VISIT:
                visit.append(student)
            case VisitStatus.NOT_VISIT:
                not_visit.append(student)

    for student in sorted(not_checked, key=lambda student: student.surname.lower()):
        none_text += telegram_link_template(student)

    for student in sorted(visit, key=lambda student: student.surname.lower()):
        visit_text += telegram_link_template(student)

    for student in sorted(not_visit, key=lambda student: student.surname.lower()):
        no_text += telegram_link_template(student)

    return f"{none_text}\n{visit_text}\n{no_text}\nЧто-то еще?"
