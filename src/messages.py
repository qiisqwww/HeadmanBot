from src.enums import VisitStatus
from src.services import AttendanceService, StudentService

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
    "GROUP_DOESNT_EXISTS_MESSAGE",
    "LOOK_WHAT_I_FOUND_MESSAGE"
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
Введите пароль старосты
Чтобы узнать пароль старосты напишите администратору - @qiisqwww"""

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
На какие сегодняшие пары ты придешь?

Если возникли проблемы - напишите о них в @noheadproblemsbot"""

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

*ВНИМАНИЕ!!!* Бот находится на стадии разработки, потому, к сожалению, пероидически могут возникать неполадки.
Если есть вопросы или предложения - вы можете написать их *сюда --->>> @noheadproblemsbot*
Благодарим за понимание
"""

GROUP_DOESNT_EXISTS_MESSAGE = "Такой группы нет!"

LOOK_WHAT_I_FOUND_MESSAGE = "Смотри что я нашел по твоему запросу:"


async def attendance_for_headmen_message(lesson_id: int, headman_id: int) -> str:
    visit_text = "Придут:\n"
    none_text = "Не отметились:\n"
    no_text = "Не придут:\n"

    not_visit = []
    visit = []
    not_checked = []

    async with StudentService() as student_service:
        headman = await student_service.get(headman_id)
        users = await student_service.filter_by_group(headman.group_id)

    user_link = '<a href="tg://user?id={user_id}">{surname} {name}</a>\n'

    async with AttendanceService() as attendance_service:
        for user in users:
            attendance = await attendance_service.get(user.telegram_id)
            attendance_lesson = tuple(filter(lambda el: el[0].id == lesson_id, attendance.lessons))[0]

            match attendance_lesson[1]:
                case VisitStatus.NOT_CHECKED:
                    not_checked.append(
                        [
                            f"{user.surname} {user.name}",
                            user_link.format(user_id=user.telegram_id, surname=user.surname, name=user.name),
                        ]
                    )
                case VisitStatus.VISIT:
                    visit.append(
                        [
                            f"{user.surname} {user.name}",
                            user_link.format(user_id=user.telegram_id, surname=user.surname, name=user.name),
                        ]
                    )
                case VisitStatus.NOT_VISIT:
                    not_visit.append(
                        [
                            f"{user.surname} {user.name}",
                            user_link.format(user_id=user.telegram_id, surname=user.surname, name=user.name),
                        ]
                    )

        for user in sorted(not_checked, key=lambda s: s[0]):
            none_text += user[1]

        for user in sorted(visit, key=lambda s: s[0]):
            visit_text += user[1]

        for user in sorted(not_visit, key=lambda s: s[0]):
            no_text += user[1]

        attendance = none_text + "\n" + visit_text + "\n" + no_text + "\n" + "Что-то еще?"

        return attendance
