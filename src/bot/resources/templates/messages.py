from asyncpg.pool import PoolConnectionProxy

from src.dto import Lesson, Student
from src.enums import VisitStatus

__all__ = [
    "HEADMAN_OR_STUDENT_MESSAGE",
    "YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE",
    "INCORRECT_DATA_MESSAGE",
    "UNSUCCESFULLY_REG_MESSAGE",
    "UNSUCCESFULL_STAROSTA_REG_MESSAGE",
    "ALL_MESSAGE",
    "NONE_MESSAGE",
    "attendance_for_headmen_message",
    "NO_LESSONS_TODAY",
    "CHOOSE_PAIR_MESSAGE",
    "POLL_MESSAGE",
    "HEADMAN_SEND_MSG_MISTAKE",
    "FAQ_MESSAGE",
    "WHICH_PAIR_MESSAGE",
]


HEADMAN_OR_STUDENT_MESSAGE = """
Ты студент или староста?"""

YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE = """
Ваша группа еще не зарегестрирована.
Для регистрации попросите вашего старосту зарегестрироваться в боте,
после чего попробуйте снова"""

INCORRECT_DATA_MESSAGE = """
Данные введены неверно. Введите еще раз."""


UNSUCCESFULLY_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова"""


UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""

WHICH_PAIR_MESSAGE = """
Какая пара вас интересует?"""


ALL_MESSAGE = """
Вы посетите все пары"""

NONE_MESSAGE = """
Вы не посетите пары """

NO_LESSONS_TODAY = """
Сегодня нет пар!"""

CHOOSE_PAIR_MESSAGE = """
Выберите пару из списка:"""

POLL_MESSAGE = """
На какие сегодняшие пары ты придешь?

Если возникли проблемы - напишите о них в @noheadproblemsbot"""

HEADMAN_SEND_MSG_MISTAKE = """
Произошла какая-то ошибка, и я не могу отправтить тебе информацию!"""

FAQ_MESSAGE = """
<b>Grand Headman MIREA был разработан как инструмент-помощник для старост.</b>


Каждый учебный день, в 07:00, бот рассылает студентам сообщение с опросом. В нем студент должен отметить,
на каких парах он обещает присутствовать. 

<b>Доступно несколько вариантов ответа:</b>
1. Студент отмечает, что придет на все пары.
2. Студент отмечает, что сегодня его в университете не будет
3. Студент указывает конкретные пары, которые он обещает посетить. На все остальные пары он автоматически будет записан, как отсутствующий.

<b>Опрос ограничен по времени.</b> Отметиться можно с в промежутке между 7 утра и концом первой <b>(по счету)</b> пары вашей группы.

Старостам доступна команда, отправляющая информацию о посещаемости группы на текущий момент - <b>/getstat</b>.

<b>ВНИМАНИЕ!!!</b> Бот находится на стадии разработки, потому, к сожалению, пероидически могут возникать неполадки.
Если есть вопросы или предложения - вы можете написать их <b>сюда --->>> @noheadproblemsbot</b>
Благодарим за понимание
"""


async def attendance_for_headmen_message(lesson: Lesson, headman: Student, con: PoolConnectionProxy) -> str:
    visit_text = "Придут:\n"
    none_text = "Не отметились:\n"
    no_text = "Не придут:\n"

    not_visit: list[Student] = []
    visit: list[Student] = []
    not_checked: list[Student] = []

    attendance_service = AttendanceService(con)
    attendances = await attendance_service.get_visit_status_for_group_students(headman.group_id, lesson)

    for student, visit_status in attendances.items():
        match visit_status:
            case VisitStatus.NOT_CHECKED:
                not_checked.append(student)
            case VisitStatus.VISIT:
                visit.append(student)
            case VisitStatus.NOT_VISIT:
                not_visit.append(student)

    for student in sorted(not_checked, key=lambda student: student.fullname.lower()):
        none_text += student.telegram_link

    for student in sorted(visit, key=lambda student: student.fullname.lower()):
        visit_text += student.telegram_link

    for student in sorted(not_visit, key=lambda student: student.fullname.lower()):
        no_text += student.telegram_link

    return none_text + "\n" + visit_text + "\n" + no_text + "\n" + "Что-то еще?"
