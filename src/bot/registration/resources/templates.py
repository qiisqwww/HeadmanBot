from src.bot.common.render_template import render_template
from src.modules.student_management.domain import Role

__all__ = [
    "student_send_registration_request_template",
    "start_message_template",
    "asking_fullname_validation_template",
    "CHOOSE_STUDENT_ROLE_TEMPLATE",
    "REGISTRATION_DENIED_TEMPLATE",
    "registration_accepted_template",
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
    "FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE",
    "FAILED_TO_FETCH_SCHEDULE_TEMPLATE",
    "HELP_FOR_HEADMAN",
    "USER_HAS_ALREADY_BEEN_REGISTERED_TEMPLATE",
    "USER_REGISTRATION_TIME_OUT_TEMPLATE",

]


CHOOSE_STUDENT_ROLE_TEMPLATE = "Нажмите на кнопку 'Я студент' или 'Я староста', чтобы выбрать свою роль."

INCORRECT_STUDENT_ROLE_TEMPLATE = "Пожалуйста, нажмите на одну из кнопок выше, чтобы выбрать вашу роль."

REGISTRATION_DENIED_TEMPLATE = "Вы отказали пользователю в регистрации."


YOU_WERE_ACCEPTED_TEMPLATE = "Ваше заявление на регистрацию было одобрено."

HELP_FOR_HEADMAN = """
<b>Как пользоваться ботом:</b>

1. Попросите студентов Вашей группы зарегистрироваться. Вам нужно просто отправить в беседу группы ссылку на бота и подождать, пока группа пройдет регистрацию.
Старосте нужно будет лишь одобрить регистрацию студента (бот отправит в ЛС сообщение с запросом).
Ссылка: @grand_headman_bot

2. В 7:00 увидеть рассылку от бота и отметиться в ней, нажав на соответствующие кнопки. То же самое должна сделать вся ваша группа.

3. Отправить боту сообщение "Узнать посещаемость" или нажать на кнопку в доступной Вам панели внизу. Вы получите доступ к списку студентов с информацией о планируемой посещаемости вашей группы на текущий день.

Если у Вас остались какие-либо вопросы, можете задать их в личные сообщения разработчикам: @neo_the_dev или @qiisqwww
"""

YOU_WERE_DENIED_TEMPLATE = """
Ваше заявление на регистрацию было отклонено.

Если вы считаете, что это была ошибка, обратитесь к своему старосте или напишите в службу обратной связи --- @noheadproblemsbot"""

ASK_UNIVERSITY_TEMPLATE = "Выберите свой университет."

INCORRECT_UNIVERSITY_TEMPLATE = "Нажмите только на одну из кнопок выше, чтобы выбрать ваш университет."

ASK_GROUP_TEMPLATE = "Введите название вашей группы"

GROUP_DOESNT_EXISTS_TEMPLATE = (
    "В выбранном университете такой группы нет. Попробуйте ввести группу заново, используя заглавные буквы"
)

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

GROUP_DOESNT_REGISTERED_TEMPLATE = """Группа еще не зарегистрирована в боте.
Попросите своего старосту зарегистрироваться, или введите название группы заново."""

TOO_MUCH_NAME_LENGTH_TEMPLATE = "Имя должно быть длиной не более 255 символов. Попробуйте снова."

TOO_MUCH_SURNAME_LENGTH_TEMPLATE = "Фамилия должно быть длиной не более 255 символов. Попробуйте снова."

WHAT_DO_YOU_WANNA_EDIT_TEMPLATE = "Что вы желаете изменить?"

FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE = (
    "Не удалось проверить наличие группы в университете, попробуйте снова или напишите в @noheadproblemsbot."
)

FAILED_TO_FETCH_SCHEDULE_TEMPLATE = (
    "Не удалось загрузить расписание для вашей группы. "
    "Попробуйте зарегистрироваться еще раз или напишите в @noheadproblemsbot."
)

USER_HAS_ALREADY_BEEN_REGISTERED_TEMPLATE = """
Пользователь уже был зарегистрирован"""

USER_REGISTRATION_TIME_OUT_TEMPLATE = """
Данные пользователя не были найдены в кеше. Либо пользователь их удалил (нажал "Зарегистрироваться заново"),
либо прошла 1 неделя."""


def successful_role_choose_template(role: Role) -> str:
    return render_template(
        "Роль была успешно выбрана. Вы - <b>{{role.translation}}</b>.",
        role=role,
    )


def successful_university_choose_template(university_name: str) -> str:
    return render_template(
        "Вы успешно выбрали университет <b>{{university_name}}</b>.",
        university_name=university_name,
    )


def student_send_registration_request_template(
    last_name: str,
    first_name: str,
    role: Role,
    telegram_id: int,
    group: str,
    username: str | None,
) -> str:
    return render_template(
        """{{role.translation}} <a href='tg://user?id={{telegram_id}}'>{{ fullname }}</a> @{{ username }}
подал заявку на регистарцию в боте в группу - {{ group }}.""",
        role=role,
        telegram_id=telegram_id,
        fullname=f"{last_name} {first_name}",
        username=username if username is not None else "",
        group=group,
    )

def registration_accepted_template(
    last_name: str,
    first_name: str,
    role: Role,
    telegram_id: int,
    username: str | None,
) -> str:
    return render_template(
        """{{role.translation}} <a href='tg://user?id={{telegram_id}}'>{{ fullname }}</a> @{{ username }}
был успешно зарегистрирован в бота.""",
        role=role,
        telegram_id=telegram_id,
        fullname=f"{last_name} {first_name}",
        username=username if username is not None else "",
    )

def start_message_template(last_name: str | None, first_name: str) -> str:
    return render_template(
        "Приветствую {% if last_name is not none %} {{last_name}} {% endif %} {{first_name}}! "
        "Для начала, давай зарегистрируемся в системе бота.",
        last_name=last_name,
        first_name=first_name,
    )


def chosen_lesson_template(lesson_name: str, start_time: str) -> str:
    return render_template(
        "Вы посетите пару {{lesson_name}}, которая начнётся в {{start_time}}",
        lesson_name=lesson_name,
        start_time=start_time,
    )


def asking_fullname_validation_template(last_name: str, first_name: str) -> str:
    return render_template(
        "{{last_name}} {{first_name}}\n\nДанные верны?",
        last_name=last_name,
        first_name=first_name,
    )


def your_choice_is_template(is_fullname_correct: bool) -> str:
    return render_template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        is_fullname_correct=is_fullname_correct,
    )
