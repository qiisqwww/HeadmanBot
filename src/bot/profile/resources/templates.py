from datetime import date

from jinja2 import Template

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
    FAILED_TO_LOAD_EDU_INFO_TEMPLATE,
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE",
]


ASK_NEW_NAME_TEMPLATE = "Введите новое имя"

ASK_NEW_SURNAME_TEMPLATE = "Введите новую фамилию"

ASK_NEW_BIRTHDATE_TEMPLATE = "Введите дату рождения (или введите 0, если не хотите ее указывать)"

NEW_BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели данные в неккорректном формате"

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы хотите отредактировать?"

FAILED_TO_LOAD_EDU_INFO_TEMPLATE = "Не удалось загрузить информацию о пользователе. Попробробуйте снова или напишете в @noheadproblemsbot."


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    template = Template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.last_name}}\n"
        "Имя: {{student.first_name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {{edu_info.group_name}}\n"
        "Университет: {{edu_info.university_name}}\n"
        "Дата рождения: {% if student.birthdate is not none %} {{student.birthdate}} {% else %}не указана {% endif %}",
        autoescape=True,
    )

    return template.render(student=student, edu_info=edu_info)


def asking_name_validation_template(first_name: str) -> str:
    template = Template("Ваше новое имя: {{first_name}}\n\nДанные верны?", autoescape=True)
    return template.render(first_name=first_name)


def asking_surname_validation_template(last_name: str) -> str:
    template = Template("Ваша новая фамилия: {{last_name}}\n\nДанные верны?", autoescape=True)
    return template.render(last_name=last_name)


def asking_birthdate_validation_template(new_birthdate: date | None) -> str:
    template = Template(
        "Ваша новая дата рождения: {% if new_birthdate is not none %} {{new_birthdate}} {% else %}не указана {% endif %}\n\nДанные верны?",
        autoescape=True,
    )
    return template.render(new_birthdate=new_birthdate)
