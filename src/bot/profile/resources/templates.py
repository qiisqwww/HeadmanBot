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
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE"
]


ASK_NEW_NAME_TEMPLATE = "Введите новое имя"

ASK_NEW_SURNAME_TEMPLATE = "Введите новую фамилию"

ASK_NEW_BIRTHDATE_TEMPLATE = "Введите дату рождения (или введите 0, если не хотите ее указывать)"

NEW_BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели данные в неккорректном формате"

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы хотите отредактировать?"


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    template = Template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.surname}}\n"
        "Имя: {{student.name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {{edu_info.group_name}}\n"
        "Университет: {{edu_info.university_name}}\n"
        "Дата рождения: {% if student.birthdate is not none %} {{student.birthdate}} {% else %}не указана {% endif %}",
        autoescape=True,
    )

    return template.render(student=student, edu_info=edu_info)


def asking_name_validation_template(name: str) -> str:
    template = Template("Ваше новое имя: {{name}}\n\nДанные верны?", autoescape=True)
    return template.render(name=name)


def asking_surname_validation_template(surname: str) -> str:
    template = Template("Ваша новая фамилия: {{surname}}\n\nДанные верны?", autoescape=True)
    return template.render(surname=surname)


def asking_birthdate_validation_template(birthdate: date | str) -> str:
    template = Template("Ваша новая дата рождения: {{birthdate}}\n\nДанные верны?", autoescape=True)
    return template.render(birthdate=birthdate)

