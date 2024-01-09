from src.modules.student_management.domain import EduProfileInfo, Student

__all__ = [
    "profile_info",
    "asking_name_validation_template",
    "asking_surname_validation_template",
]


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    return (
        f"<b>Профиль студента</b>\n\n"
        f"Фамилия: <i>{student.surname}</i>\n"
        f"Имя: <i>{student.name}</i>\n"
        f"Роль: <i>{student.role.translation}</i>\n"
        f"Группа: <i>{edu_info.group_name}</i>\n"
        f"Университет: <i>{edu_info.university_name}</i>\n"
    )


def asking_name_validation_template(name: str) -> str:
    return f"Ваше новое имя: {name}\n\nДанные верны?"


def asking_surname_validation_template(surname: str) -> str:
    return f"Ваша новая фамилия: {surname}\n\nДанные верны?"
