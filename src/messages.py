from asyncpg.pool import PoolConnectionProxy

from src.dto import Lesson, Student
from src.enums import VisitStatus
from src.services import AttendanceService

__all__ = [
    "START_MESSAGE",
    "ASK_GROUP_MESSAGE",
    "HEADMAN_OR_STUDENT_MESSAGE",
    "YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE",
    "INCORRECT_DATA_MESSAGE",
    "ASK_SURNAME_MESSAGE",
    "ASK_NAME_MESSAGE",
    "YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE",
    "YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE",
    "REGISTRATION_DENIED_MESSAGE",
    "REGISTRATION_ACCEPTED_MESSAGE",
    "YOU_WERE_ACCEPTED_MESSAGE",
    "YOU_WERE_DENIED_MESSAGE",
    "UNSUCCESFULLY_REG_MESSAGE",
    "STAROSTA_REG_MESSAGE",
    "UNSUCCESFULL_STAROSTA_REG_MESSAGE",
    "MUST_BE_REG_MESSAGE",
    "MUST_BE_HEADMEN_MESSAGE",
    "ALREADY_REGISTERED_MESSAGE",
    "ALL_MESSAGE",
    "NONE_MESSAGE",
    "attendance_for_headmen_message",
    "NO_LESSONS_TODAY",
    "CHOOSE_PAIR_MESSAGE",
    "POLL_MESSAGE",
    "HEADMAN_SEND_MSG_MISTAKE",
    "FAQ_MESSAGE",
    "GROUP_DOESNT_EXISTS_MESSAGE",
    "LOOK_WHAT_I_FOUND_MESSAGE",
    "WHICH_PAIR_MESSAGE",
]

START_MESSAGE = """
Приветствую! Для начала, давай зарегестрируемся в системе бота.
Выбери свой университет из предложенных в списке:"""

ASK_GROUP_MESSAGE = """
Отлично! Теперь отправь мне название своей группы"""

HEADMAN_OR_STUDENT_MESSAGE = """
Ты студент или староста?"""

YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE = """
Ваша группа еще не зарегестрирована.
Для регистрации попросите вашего старосту зарегестрироваться в боте,
после чего попробуйте снова"""

INCORRECT_DATA_MESSAGE = """
Данные введены неверно. Введите еще раз."""

ASK_SURNAME_MESSAGE = """
Отправь свою фамилию"""

ASK_NAME_MESSAGE = """
Отправь свое имя"""

YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE = """
Ваше заявление на регистрацию старостой было передано администраторам."""

YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE = """
Ваше заявление на регистрацию студентом было передано старосте."""

REGISTRATION_DENIED_MESSAGE = """
Вы отказали пользователю в регистрации."""

REGISTRATION_ACCEPTED_MESSAGE = """
Пользователь был успешно зарегестрирован."""

YOU_WERE_ACCEPTED_MESSAGE = """
Ваше заявление на регистрацию было одобрено."""

YOU_WERE_DENIED_MESSAGE = """
Ваше заявление на регистрацию было отклонено.

Если вы считаете, что это была ошибка, обратитесь к своему старосте или
напишите в службу обратной связи --- @noheadproblemsbot"""

UNSUCCESFULLY_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова"""

ALREADY_REGISTERED_MESSAGE = """
Ты уже зарегестрирован в системе"""

UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""

WHICH_PAIR_MESSAGE = """
Какая пара вас интересует?"""

MUST_BE_REG_MESSAGE = """
Для выполнения данной команды вы должны быть зарегестрированы! (/start)"""

MUST_BE_HEADMEN_MESSAGE = """
Для выполнения данной команды вы должны быть старостой."""

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

GROUP_DOESNT_EXISTS_MESSAGE = "Такой группы нет!"

LOOK_WHAT_I_FOUND_MESSAGE = "Смотри что я нашел по твоему запросу:"


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

    for student in sorted(not_checked, key=lambda student: student.fullname):
        none_text += student.telegram_link

    for student in sorted(visit, key=lambda student: student.fullname):
        visit_text += student.telegram_link

    for student in sorted(not_visit, key=lambda student: student.fullname):
        no_text += student.telegram_link

    return none_text + "\n" + visit_text + "\n" + no_text + "\n" + "Что-то еще?"
