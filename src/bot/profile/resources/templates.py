from datetime import date

from src.bot.common.render_template import render_template
from src.modules.student_management.domain import EduProfileInfo, Student

__all__ = [
    "profile_info",
    "asking_name_validation_template",
    "asking_surname_validation_template",
    "asking_birthdate_validation_template",
    "your_choice_is_template",
    "ASK_NEW_SURNAME_TEMPLATE",
    "ASK_NEW_NAME_TEMPLATE",
    "ASK_NEW_BIRTHDATE_TEMPLATE",
    "NEW_BIRTHDATE_INCORRECT_TEMPLATE",
    "FAILED_TO_LOAD_EDU_INFO_TEMPLATE",
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE",
    "SURE_TO_LEAVE_GROUP_TEMPLATE",
    "SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE"
]


ASK_NEW_NAME_TEMPLATE = "Введите новое имя"

ASK_NEW_SURNAME_TEMPLATE = "Введите новую фамилию"

ASK_NEW_BIRTHDATE_TEMPLATE = """Введите дату рождения в формате ДД.ММ.ГГГГ.
Если вы не хотите указывать свою дату рождения, введите 0"""

NEW_BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели данные в неккорректном формате"

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы хотите отредактировать?"

FAILED_TO_LOAD_EDU_INFO_TEMPLATE = """Не удалось загрузить информацию о пользователе. 
Попробробуйте снова или напишете в @noheadproblemsbot."""

SURE_TO_LEAVE_GROUP_TEMPLATE = """Вы уверены, что хотите выйти из группы?"""

SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE = """Вы успешно вышли из группы"""


# TODO: разобраться в ошибке, из-за которой не выводится "отсутствует" у группы и университета
def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    return render_template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.last_name}}\n"
        "Имя: {{student.first_name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {% if edu_info.group_name is not none %} {{edu_info.group_name}}\n{% else %} отсутствует\n{% endif %}"  
        "Университет: {{edu_info.university_name}}\n"
        "Дата рождения: {% if student.birthdate is not none %} {{student.birthdate}} {% else %} не указана {% endif %}",
        student=student,
        edu_info=edu_info,
    )


def asking_name_validation_template(first_name: str) -> str:
    return render_template(
        "Ваше новое имя: <b>{{first_name}}</b>\n\nДанные верны?",
        first_name=first_name,
    )


def asking_surname_validation_template(last_name: str) -> str:
    return render_template(
        "Ваша новая фамилия: <b>{{last_name}}</b>\n\nДанные верны?",
        last_name=last_name,
    )


def asking_birthdate_validation_template(new_birthdate: date | None) -> str:
    return render_template(
        """Ваша новая дата рождения: {% if new_birthdate is not none %} <b>{{new_birthdate}}</b>
        {% else %}<b>не указана </b>{% endif %}"""
        "\n\nДанные верны?",
        new_birthdate=new_birthdate,
    )


def your_choice_is_template(choice: bool) -> str:
    return render_template(
        "Вы выбрали: {% if choice %} <b>Да</b> {% else %} <b>Нет</b> {% endif %}",
        choice=choice,
    )
