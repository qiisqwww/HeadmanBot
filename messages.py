from aiogram import types

from service import UsersService

__all__ = ["START_MESSAGE", "REG_MESSAGE_1", "REG_MESSAGE_2",
           "SUCCESFULLY_REG_MESSAGE", "UNSUCCESFULLY_REG_MESSAGE", "PASS_ASK_MESSAGE",
           "STAROSTA_REG_MESSAGE", "UNSUCCESFULL_STAROSTA_REG_MESSAGE", "ALREADY_HEADMAN_MESSAGE",
           "MUST_BE_REG_MESSAGE", "MUST_BE_HEADMEN_MESSAGE", "ALREADY_REGISTERED_MESSAGE",
           "WRONG_PASSWORD", "ALL_MESSAGE", "NONE_MESSAGE", "load_attendance_for_headmen",
           "NO_LESSONS_TODAY", "CHOOSE_GETSTAT_LESSON", "POLL_MESSAGE"]

START_MESSAGE = """
Привет! Я - твоя староста!"""

REG_MESSAGE_1 = """
Для начала, напомни, как тебя зовут? (И фамилию)"""

REG_MESSAGE_2 = """
Из какой ты группы? (!Вводить строго в формате ХХХХ-ХХ-ХХ!)"""

SUCCESFULLY_REG_MESSAGE = """
Ты был успешно зарегестрирован в системе!"""

UNSUCCESFULLY_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова!"""

ALREADY_REGISTERED_MESSAGE = """
Ты уже зарегестрирован в системе!"""

PASS_ASK_MESSAGE = """
Введите пароль старосты"""

STAROSTA_REG_MESSAGE = """
Вы были успешно зарегестрированы как староста!"""

UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""

ALREADY_HEADMAN_MESSAGE = """
Вы и так зарегестрированы как староста!"""

MUST_BE_REG_MESSAGE = """
Для выполнения данной команды вы должны быть зарегестрированы! (/start)"""

MUST_BE_HEADMEN_MESSAGE = """
Для выполнения данной команды вы должны быть старостой.
Для регистрации как страоста - /set_headmen"""

WRONG_PASSWORD = """
Вы ввели неверный пароль!"""

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


def load_attendance_for_headmen(message: types.Message) -> str:
    visit_text = 'Придут:\n'
    none_text = 'Не отметились:\n'
    no_text = 'Не придут:\n'
    try:
        lesson = int(message.text.split(') ')[0]) - 1
    except Exception as e:
        return "Вы ввели неверные данные!"

    no_visit = []
    none_checked_in = []
    visit = []

    with UsersService() as con:
        group = con.get_group_of_id_tg(message.from_user.id)

        for user_id in con.get_user_of_group(group):
            user_id = user_id[0]
            print(con.get_lessons(user_id))
            if len(con.get_lessons(user_id).replace('0', '')) == 0:
                none_checked_in.append(user_id)
                continue
            match con.get_lessons(user_id)[lesson]:
                case '0':  # мне лень при нажатии на кнопку я приду на пару n обновлять всю
                    # бд тем, что я не приду, поэтому я встроил такую проверку, да пиздец,
                    # но я на семинаре по процедурке, у меня есть ещё пара дел
                    no_visit.append(user_id)
                case '1':
                    visit.append(user_id)
                case '2':
                    no_visit.append(user_id)

        for user in none_checked_in:
            none_text += str(con.get_user_of_id_tg(user)[2]) + ' @' + str(con.get_user_of_id_tg(user)[1]) + '\n'
        for user in visit:
            visit_text += str(con.get_user_of_id_tg(user)[2]) +  ' @' + str(con.get_user_of_id_tg(user)[1]) + '\n'
        for user in no_visit:
            no_text += str(con.get_user_of_id_tg(user)[2]) +  ' @' + str(con.get_user_of_id_tg(user)[1]) + '\n'

        attendance = none_text + '\n' + visit_text + '\n' + no_text + '\n'

        return attendance
