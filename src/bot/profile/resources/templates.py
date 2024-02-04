from jinja2 import Template

from src.modules.student_management.domain import EduProfileInfo, Student

__all__ = [
    "profile_info",
    "asking_name_validation_template",
    "asking_surname_validation_template",
]


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    template = Template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.surname}}\n"
        "Имя: {{student.name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {{edu_info.group_name}}\n"
        "Университет: {{edu_info.university_name}}\n"
        "Дата рождения: {% if student.birthdate is not none %} {{student.birthdate}} {% else %} не указана {% endif %}",
        autoescape=True,
    )

    return template.render(student=student, edu_info=edu_info)


def asking_name_validation_template(name: str) -> str:
    template = Template("Ваше новое имя: {{name}}\n\nДанные верны?", autoescape=True)
    return template.render(name=name)


def asking_surname_validation_template(surname: str) -> str:
    template = Template("Ваша новая фамилия: {{surname}}\n\nДанные верны?", autoescape=True)
    return template.render(surname=surname)
