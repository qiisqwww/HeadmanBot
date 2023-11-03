from aiogram import types

from .services import UsersService

__all__ = [
    "START_MESSAGE",
    "REG_MESSAGE_1_1",
    "REG_MESSAGE_1_2",
    "REG_MESSAGE_2",
    "SUCCESFULLY_REG_MESSAGE",
    "UNSUCCESFULLY_REG_MESSAGE",
    "PASS_ASK_MESSAGE",
    "STAROSTA_REG_MESSAGE",
    "UNSUCCESFULL_STAROSTA_REG_MESSAGE",
    "ALREADY_HEADMAN_MESSAGE",
    "MUST_BE_REG_MESSAGE",
    "MUST_BE_HEADMEN_MESSAGE",
    "ALREADY_REGISTERED_MESSAGE",
    "WRONG_PASSWORD",
    "ALL_MESSAGE",
    "NONE_MESSAGE",
    "attendance_for_headmen_message",
    "NO_LESSONS_TODAY",
    "CHOOSE_GETSTAT_LESSON",
    "POLL_MESSAGE",
    "HEADMAN_SEND_MSG_MISTAKE",
    "FAQ_MESSAGE",
]

START_MESSAGE = """
Привет! Я - помощник твоей старосты"""

REG_MESSAGE_1_1 = """
Для начала, введи свою фамилию"""

REG_MESSAGE_1_2 = """
Теперь отправь мне свое имя"""

REG_MESSAGE_2 = """
Из какой ты группы? (!Вводить строго в формате ХХХХ-ХХ-ХХ!)"""

SUCCESFULLY_REG_MESSAGE = """
Ты был успешно зарегестрирован в системе!
Если вы - староста, пропишите /set_headman"""

UNSUCCESFULLY_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова!"""

ALREADY_REGISTERED_MESSAGE = """
Ты уже зарегестрирован в системе!"""

PASS_ASK_MESSAGE = """
Введите пароль старосты"""

STAROSTA_REG_MESSAGE = """
Вы были успешно зарегестрированы как староста!
Чтобы получить информацию о функционале бота, введите команду /faq"""

UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""

ALREADY_HEADMAN_MESSAGE = """
Вы и так зарегестрированы как староста!"""

MUST_BE_REG_MESSAGE = """
Для выполнения данной команды вы должны быть зарегестрированы! (/start)"""

MUST_BE_HEADMEN_MESSAGE = """
Для выполнения данной команды вы должны быть старостой.
Для регистрации как староста - /set_headman"""

WRONG_PASSWORD = """
Вы ввели неверный пароль!
Если вы староста, но у вас нет пароля - обратитесь к @qiisqwww"""

ALL_MESSAGE = """
Вы посетите все пары"""

NONE_MESSAGE = """
Вы не посетите пары """

NO_LESSONS_TODAY = """
Сегодня нет пар!"""

CHOOSE_GETSTAT_LESSON = """
Какая пара вас интересует?"""

POLL_MESSAGE = """
На какие сегодняшие пары ты придешь?"""

HEADMAN_SEND_MSG_MISTAKE = """
Произошла какая-то ошибка, и я не могу отправтить тебе информацию!"""

FAQ_MESSAGE = """
*Grand Headman MIREA был разработан как инструмент-помощник для старост.*


Каждый учебный день, в 07:00, бот рассылает студентам сообщение с опросом. В нем студент должен отметить,
на каких парах он обещает присутствовать. 

*Доступно несколько вариантов ответа:*
1. Студент отмечает, что придет на все пары.
2. Студент отмечает, что сегодня его в университете не будет
3. Студент указывает конкретные пары, которые он обещает посетить. На все остальные пары он автоматически будет записан, как отсутствующий.

*Опрос ограничен по времени.* Отметиться можно с в промежутке между 7 утра и концом первой *(по счету)* пары вашей группы.

Старостам доступна команда, отправляющая информацию о посещаемости группы на текущий момент - */getstat*.

*ВНИМАНИЕ!!!* В данный момент возможность перегеристрации недоступна, потому попросите студентов вводить данные при регистрации корректно.
Это в Ваших же интересах. Если возникла такая ситуация, что необходимо отредактировать введенные при регистрации данные - обращаться сюда: @qiisqwww
"""


def attendance_for_headmen_message(callback: types.CallbackQuery) -> str:
    visit_text = "Придут:\n"
    none_text = "Не отметились:\n"
    no_text = "Не придут:\n"

    lesson = int(callback.data)

    no_visit = []
    none_checked_in = []
    visit = []

    with UsersService() as con:
        group = con.get_group_of_id_tg(callback.from_user.id)

        for user_id in con.get_user_of_group(group):
            if len(con.get_lessons(user_id).replace("0", "")) == 0:
                none_checked_in.append(
                    [
                        str(con.get_user_of_id_tg(user_id)[2]),
                        f'<a href="tg://user?id={user_id}">{con.get_user_of_id_tg(user_id)[2]}</a>\n',
                    ]
                )
                continue
            match con.get_lessons(user_id)[lesson]:
                case "0":
                    no_visit.append(
                        [
                            str(con.get_user_of_id_tg(user_id)[2]),
                            f'<a href="tg://user?id={user_id}">{con.get_user_of_id_tg(user_id)[2]}</a>\n',
                        ]
                    )
                case "1":
                    visit.append(
                        [
                            str(con.get_user_of_id_tg(user_id)[2]),
                            f'<a href="tg://user?id={user_id}">{con.get_user_of_id_tg(user_id)[2]}</a>\n',
                        ]
                    )
                case "2":
                    no_visit.append(
                        [
                            str(con.get_user_of_id_tg(user_id)[2]),
                            f'<a href="tg://user?id={user_id}">{con.get_user_of_id_tg(user_id)[2]}</a>\n',
                        ]
                    )

        for user in sorted(none_checked_in, key=lambda s: s[0]):
            none_text += user[1]
        for user in sorted(visit, key=lambda s: s[0]):
            visit_text += user[1]
        for user in sorted(no_visit, key=lambda s: s[0]):
            no_text += user[1]

        attendance = none_text + "\n" + visit_text + "\n" + no_text + "\n" + "Что-то еще?"

        return attendance
