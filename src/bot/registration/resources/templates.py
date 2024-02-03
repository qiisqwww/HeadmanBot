from jinja2 import Template

from src.modules.student_management.domain import Role

__all__ = [
    "student_send_registration_request_template",
    "start_message_template",
    "asking_fullname_validation_template",
    "CHOOSE_STUDENT_ROLE_TEMPLATE",
    "REGISTRATION_DENIED_TEMPLATE",
    "REGISTRATION_ACCEPTED_TEMPLATE",
    "YOU_WERE_DENIED_TEMPLATE",
    "YOU_WERE_ACCEPTED_TEMPLATE",
    "ASK_UNIVERSITY_TEMPLATE",
    "ASK_NEW_NAME_TEMPLATE",
    "ASK_NEW_SURNAME_TEMPLATE",
    "successful_role_choose_template",
    "successful_university_choose_template",
    "ASK_GROUP_TEMPLATE",
    "INCORRECT_UNIVERSITY_TEMPLATE",
    "INCORRECT_STUDENT_ROLE_TEMPLATE",
    "GROUP_DOESNT_EXISTS_TEMPLATE",
    "ASK_NAME_TEMPLATE",
    "ASK_SURNAME_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE",
    "HEADMAN_ALREADY_EXISTS_TEMPLATE",
    "GROUP_DOESNT_REGISTERED_TEMPLATE",
    "BIRTHDATE_INCORRECT_TEMPLATE",
    "ASK_BIRTHDATE_TEMPLATE",
    "chosen_lesson_template",
    "TOO_MUCH_NAME_LENGTH_TEMPLATE",
    "TOO_MUCH_SURNAME_LENGTH_TEMPLATE",
    "your_choice_is_template",
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE",
]


CHOOSE_STUDENT_ROLE_TEMPLATE = "Нажмите на кнопку 'Я студент' или 'Я староста', чтобы выбрать свою роль."

INCORRECT_STUDENT_ROLE_TEMPLATE = "Пожалуйста, нажмите на одну из кнопок выше, чтобы выбрать вашу роль."

REGISTRATION_DENIED_TEMPLATE = "Вы отказали пользователю в регистрации."

REGISTRATION_ACCEPTED_TEMPLATE = "Пользователь был успешно зарегестрирован."

YOU_WERE_ACCEPTED_TEMPLATE = "Ваше заявление на регистрацию было одобрено."

YOU_WERE_DENIED_TEMPLATE = """
Ваше заявление на регистрацию было отклонено.

Если вы считаете, что это была ошибка, обратитесь к своему старосте или
напишите в службу обратной связи --- @noheadproblemsbot"""

ASK_UNIVERSITY_TEMPLATE = "Выберите свой университет."

INCORRECT_UNIVERSITY_TEMPLATE = "Нажмите только на одну из кнопок выше, чтобы выбрать ваш университет."

ASK_GROUP_TEMPLATE = "Введите название вашей группы"

GROUP_DOESNT_EXISTS_TEMPLATE = "В выбранном университете такой группы нет. Попробуйте ввести группу заново."

ASK_SURNAME_TEMPLATE = "Введите свою фамилию"

ASK_NAME_TEMPLATE = "Введите свое имя"

ASK_NEW_NAME_TEMPLATE = "Введите новое имя"

ASK_NEW_SURNAME_TEMPLATE = "Введите новую фамилию"

YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE = "Ваше заявление на регистрацию старостой было передано администраторам."

YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE = "Ваше заявление на регистрацию студентом было передано старосте."

ASK_BIRTHDATE_TEMPLATE = """Введите дату рождения в формате ДД.ММ.ГГГГ.
Это поможет сделать бота еще удобнее.
Если вы не хотите указывать свою дату рождения, введите 0"""

BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели некорректные данные. Введите дату в формате ДД.ММ.ГГГГ"

HEADMAN_ALREADY_EXISTS_TEMPLATE = "У выбранной группы уже есть староста."


GROUP_DOESNT_REGISTERED_TEMPLATE = """Группа не зарегистрирована в боте, попросите своего старосту ее зарегистрировать.
Попробуйте ввести название группы заново."""

TOO_MUCH_NAME_LENGTH_TEMPLATE = "Имя должно быть длиной не более 255 символов. Попробуйте снова."

TOO_MUCH_SURNAME_LENGTH_TEMPLATE = "Фамилия должно быть длиной не более 255 символов. Попробуйте снова."

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы желаете изменить?"


def successful_role_choose_template(role: Role) -> str:
    template = Template("Роль была успешно выбрана. Вы - <b>{{role.translation}}</b>.", autoescape=True)
    return template.render(role=role)


def successful_university_choose_template(university_name: str) -> str:
    template = Template("Вы успешно выбрали университет <b>{{university_name}}</b>.", autoescape=True)
    return template.render(university_name=university_name)


def student_send_registration_request_template(surname: str, name: str, role: Role, telegram_id: int) -> str:
    template = Template(
        "{{role.translation}} <a href='tg://user?id={{telegram_id}}'>{{surname}} {{name}}</a> подал заявку на регистарцию в боте.",
        autoescape=True,
    )
    return template.render(role=role, surname=surname, name=name, telegram_id=telegram_id)


def start_message_template(surname: str | None, name: str) -> str:
    template = Template(
        "Приветствую {% if surname is not none %} {{surname}} {% endif %} {{name}}! Для начала, давай зарегистрируемся в системе бота.",
        autoescape=True,
    )
    return template.render(surname=surname, name=name)


def chosen_lesson_template(lesson_name: str, start_time: str) -> str:
    template = Template("Вы посетите пару {{lesson_name}}, которая начнётся в {{start_time}}", autoescape=True)
    return template.render(lesson_name=lesson_name, start_time=start_time)


def asking_fullname_validation_template(surname: str, name: str) -> str:
    template = Template("{{surname}} {{name}}\n\nДанные верны?", autoescape=True)
    return template.render(surname=surname, name=name)


def your_choice_is_template(is_fullname_correct: bool) -> str:
    template = Template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        autoescape=True,
    )
    return template.render(is_fullname_correct=is_fullname_correct)
