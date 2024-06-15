from datetime import date

from src.bot.common.render_template import render_template
from src.modules.student_management.domain import EduProfileInfo, Student

__all__ = [
    "profile_info",
    "asking_name_validation_template",
    "asking_surname_validation_template",
    "asking_birthdate_validation_template",
    "ASK_NEW_SURNAME_TEMPLATE",
    "ASK_NEW_NAME_TEMPLATE",
    "ASK_NEW_BIRTHDATE_TEMPLATE",
    "NEW_BIRTHDATE_INCORRECT_TEMPLATE",
    "FAILED_TO_LOAD_EDU_INFO_TEMPLATE",
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE",
]


ASK_NEW_NAME_TEMPLATE = "Введите новое имя"

ASK_NEW_SURNAME_TEMPLATE = "Введите новую фамилию"

ASK_NEW_BIRTHDATE_TEMPLATE = """Введите дату рождения в формате ДД.ММ.ГГГГ.
Если вы не хотите указывать свою дату рождения, введите 0"""

NEW_BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели данные в неккорректном формате"

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы хотите отредактировать?"

FAILED_TO_LOAD_EDU_INFO_TEMPLATE = """Не удалось загрузить информацию о пользователе. 
Попробробуйте снова или напишете в @noheadproblemsbot."""


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    formatted_date = None if student.birthdate is None else student.birthdate.strftime("%d.%m.%Y")
    return render_template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.last_name}}\n"
        "Имя: {{student.first_name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {{edu_info.group_name}}\n"
        "Университет: {{edu_info.university_name}}\n"
        "Дата рождения: {% if birthdate is not none %} {{birthdate}} {% else %}не указана {% endif %}",
        student=student,
        birthdate=formatted_date,
        edu_info=edu_info,
    )


def asking_name_validation_template(first_name: str) -> str:
    return render_template(
        "Ваше новое имя: {{first_name}}\n\nДанные верны?",
        first_name=first_name,
    )


def asking_surname_validation_template(last_name: str) -> str:
    return render_template(
        "Ваша новая фамилия: {{last_name}}\n\nДанные верны?",
        last_name=last_name,
    )


def asking_birthdate_validation_template(new_birthdate: date | None) -> str:
    formatted_date = None if new_birthdate is None else new_birthdate.strftime("%d.%m.%Y")
    return render_template(
        """Ваша новая дата рождения: {% if new_birthdate is not none %} {{new_birthdate}}
        {% else %}не указана {% endif %}"""
        "\n\nДанные верны?",
        new_birthdate=formatted_date,
    )
