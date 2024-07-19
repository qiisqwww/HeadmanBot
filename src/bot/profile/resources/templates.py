from datetime import date

from src.bot.common.render_template import render_template
from src.modules.student_management.domain import EduProfileInfo, Student, Role

__all__ = [
    "profile_info",
    "asking_name_validation_template",
    "asking_surname_validation_template",
    "asking_birthdate_validation_template",
    "successful_university_choose_template",
    "successful_role_choose_template",
    "student_send_enter_group_request_template",
    "student_send_leave_group_request_template",
    "ASK_NEW_SURNAME_TEMPLATE",
    "ASK_NEW_NAME_TEMPLATE",
    "ASK_NEW_BIRTHDATE_TEMPLATE",
    "NEW_BIRTHDATE_INCORRECT_TEMPLATE",
    "FAILED_TO_LOAD_EDU_INFO_TEMPLATE",
    "WHAT_DO_YOU_WANNA_EDIT_TEMPLATE",
    "SURE_TO_LEAVE_GROUP_TEMPLATE",
    "SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE",
    "DID_NOT_LEFT_THE_GROUP_TEMPLATE",
    "INPUT_GROUP_NAME_TEMPLATE",
    "FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE",
    "GROUP_DOESNT_EXISTS_TEMPLATE",
    "CHOOSE_NEW_ROLE_TEMPLATE",
    "CHOOSE_BUTTONS_ABOVE_TEMPLATE",
    "INPUT_YOUR_UNIVERSITY_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE",
    "FAILED_TO_FETCH_SCHEDULE_TEMPLATE",
    "HELP_FOR_HEADMAN",
    "YOU_WERE_DENIED_TEMPLATE",
    "YOU_WERE_ACCEPTED_TEMPLATE",
    "USER_HAS_ALREADY_ENTERED_GROUP_TEMPLATE",
    "USER_GROUP_ENTER_TIME_OUT_TEMPLATE",
    "ENTER_DENIED_TEMPLATE",
    "ENTER_ACCEPTED_TEMPLATE",
    "HEADMAN_ALREADY_EXISTS_TEMPLATE",
    "GROUP_DOESNT_REGISTERED_TEMPLATE",
    "SUCCESSFULLY_DID_NOT_LEFT_THE_GROUP_TEMPLATE",
    "YOUR_APPLY_TO_LEAVE_WAS_SENT_TO_HEADMAN_TEMPLATE",
    "LEAVE_DENIED_TEMPLATE",
    "LEAVE_ACCEPTED_TEMPLATE",
    "USER_WAS_NOT_FOUND_TO_EXPEL_TEMPLATE"
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

YOUR_APPLY_TO_LEAVE_WAS_SENT_TO_HEADMAN_TEMPLATE = """Ваше заявление на выход из группы было отправлено вашей старосте
"""

SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE = """Староста одобрил ваш запрос на выход из группы."""

SUCCESSFULLY_DID_NOT_LEFT_THE_GROUP_TEMPLATE = """Староста отклонил ваш запрос на выход из группы.

Если вы считаете, что это была ошибка, обратитесь к своему старосте или
напишите в службу обратной связи --- @noheadproblemsbot"""

DID_NOT_LEFT_THE_GROUP_TEMPLATE = "Вы выбрали не выходить из группы"

INPUT_GROUP_NAME_TEMPLATE = """Введите название группы, в которую хотите войти"""

INPUT_YOUR_UNIVERSITY_TEMPLATE = "Выберите ваш университет"

USER_WAS_NOT_FOUND_TO_EXPEL_TEMPLATE = """Пользователь, пожелавший выйти не найден. 
Его запрос автоматически отклонен"""

FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE = (
    "Не удалось проверить наличие группы в университете, попробуйте снова или напишите в @noheadproblemsbot."
)

GROUP_DOESNT_EXISTS_TEMPLATE = (
    "В вашем университете такой группы нет. Попробуйте ввести группу заново, используя заглавные буквы"
)

CHOOSE_NEW_ROLE_TEMPLATE = "Вы староста или студент?"

CHOOSE_BUTTONS_ABOVE_TEMPLATE = "Вам нужно нажать на одну из кнопок выше."

YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE = "Ваше заявление на вход в группу старостой было передано администраторам."

YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE = "Ваше заявление на вход в группу студентом было передано старосте."

FAILED_TO_FETCH_SCHEDULE_TEMPLATE = (
    "Не удалось загрузить расписание для вашей группы. "
    "Попробуйте войти еще раз или напишите в @noheadproblemsbot."
)

HEADMAN_ALREADY_EXISTS_TEMPLATE = "У выбранной группы уже есть староста."

GROUP_DOESNT_REGISTERED_TEMPLATE = """Группа еще не зарегистрирована в боте.
Попросите своего старосту зарегестрироваться, или введите название группы заново."""

HELP_FOR_HEADMAN = """
<b>Как пользоваться ботом:</b>

1. Попросите студентов Вашей группы зарегистрироваться. Вам нужно просто отправить в беседу группы ссылку на бота и подождать, пока группа пройдет регистрацию.
Старосте нужно будет лишь одобрить регистрацию студента (бот отправит в ЛС сообщение с запросом).
Ссылка: @grand_headman_bot

2. В 7:00 увидеть рассылку от бота и отметиться в ней, нажав на соответствующие кнопки. То же самое должна сделать вся ваша группа.

3. Отправить боту сообщение "Узнать посещаемость" или нажать на кнопку в доступной Вам панели внизу. Вы получите доступ к списку студентов с информацией о планируемой посещаемости вашей группы на текущий день.

Если у Вас остались какие-либо вопросы, можете задать их в личные сообщения разработчикам: @neothebest228 или @qiisqwww
"""

YOU_WERE_DENIED_TEMPLATE = """
Ваше заявление на вход было отклонено.

Если вы считаете, что это была ошибка, обратитесь к своему старосте или
напишите в службу обратной связи --- @noheadproblemsbot"""

ENTER_DENIED_TEMPLATE = "Вы отказали пользователю во входе."

LEAVE_DENIED_TEMPLATE = "Вы отказали пользователю в выходе."

LEAVE_ACCEPTED_TEMPLATE = "Пользователь успешно вышел из группы."

ENTER_ACCEPTED_TEMPLATE = "Пользователь был успешно добавлен в группу."

YOU_WERE_ACCEPTED_TEMPLATE = "Ваше заявление на вход в группу было одобрено."

USER_HAS_ALREADY_ENTERED_GROUP_TEMPLATE = """
Пользователь уже вошел в группу"""

USER_GROUP_ENTER_TIME_OUT_TEMPLATE = """
Данные пользователя не были найдены в кеше. Либо пользователь их удалил (нажал "Войти в группу" заново), 
либо прошла 1 неделя."""


def profile_info(student: Student, edu_info: EduProfileInfo) -> str:
    return render_template(
        "<b>Профиль студента</b>\n\n"
        "Фамилия: {{student.last_name}}\n"
        "Имя: {{student.first_name}}\n"
        "Роль: {{student.role.translation}}\n"
        "Группа: {% if edu_info.group_name is not none %} {{edu_info.group_name}}\n{% else %} Отсутствует\n{% endif %}"  
        "Университет: {% if edu_info.university_name is not none %} {{edu_info.university_name}}\n{% else %} "
        "Отсутствует\n{% endif %}"
        "Дата рождения: {% if student.birthdate is not none %} {{student.birthdate}} {% else %} Не указана {% endif %}",
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


def successful_university_choose_template(university_name: str) -> str:
    return render_template(
        "Вы успешно выбрали университет <b>{{university_name}}</b>.",
        university_name=university_name,
    )


def successful_role_choose_template(role: Role) -> str:
    return render_template(
        "Роль была успешно выбрана. Вы - <b>{{role.translation}}</b>.",
        role=role,
    )


def student_send_enter_group_request_template(
    last_name: str,
    first_name: str,
    role: Role,
    telegram_id: int,
    username: str | None,
) -> str:
    return render_template(
        """{{role.translation}} <a href='tg://user?id={{telegram_id}}'>{{ fullname }}</a> @{{ username }}
подал заявку на вход в группу в боте.""",
        role=role,
        telegram_id=telegram_id,
        fullname=f"{last_name} {first_name}",
        username=username if username is not None else "",
    )


def student_send_leave_group_request_template(
    last_name: str,
    first_name: str,
    role: Role,
    telegram_id: int,
    username: str | None,
) -> str:
    return render_template(
        """{{role.translation}} <a href='tg://user?id={{telegram_id}}'>{{ fullname }}</a> @{{ username }}
подал заявку на выход из вашей группы в боте.""",
        role=role,
        telegram_id=telegram_id,
        fullname=f"{last_name} {first_name}",
        username=username if username is not None else "",
    )
