from src.modules.student.internal.enums import Role

__all__ = [
    "start_message_template",
    "CHOOSE_STUDENT_ROLE_TEMPLATE",
    "REGISTRATION_DENIED_TEMPLATE",
    "REGISTRATION_ACCEPTED_TEMPLATE",
    "YOU_WERE_DENIED_TEMPLATE",
    "YOU_WERE_ACCEPTED_TEMPLATE",
    "ASK_UNIVERSITY_TEMPLATE",
    "succesfull_role_choose_template",
    "succesfull_university_choose_template",
    "ASK_GROUP_TEMPLATE",
    "INCORRECT_UNIVERSITY_TEMPLATE",
    "INCORRECT_STUDENT_ROLE_TEMPLATE",
    "GROUP_DOESNT_EXISTS_TEMPLATE",
    "ASK_NAME_TEMPLATE",
    "ASK_SURNAME_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE",
    "YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE",
    "ASK_BIRTHMONTH_TEMPLATE",
    "ASK_BIRTHDAY_TEMPLATE",
    "BIRTHMONTH_MUST_BE_DIGIT_TEMPLATE",
    "BIRTHMONTH_INCORRECT_TEMPLATE",
    "BIRTHDAY_MUST_BE_DIGIT_TEMPLATE",
    "BIRTHDAY_INCORRECT_TEMPLATE",
    "GROUP_ALREADY_EXISTS_TEMPLATE",
    "FAQ_TEMPLATE",
]


def start_message_template(surname: str | None, name: str) -> str:
    if surname is None:
        return f"Приветствую {name}! Для начала, давай зарегистрируемся в системе бота."
    return f"Приветствую {surname} {name}! Для начала, давай зарегистрируемся в системе бота."


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
INCORRECT_UNIVERSITY_TEMPLATE = "Пожалуйста, нажмите на одну из кнопок выше, чтобы выбрать ваш университет."


def succesfull_role_choose_template(role: Role) -> str:
    return f"Отлично, роль выбрана, вы теперь - <b>{role}</b>."


def succesfull_university_choose_template(university_name: str) -> str:
    return f"Отлично, выбран университет - <b>{university_name}</b>."


ASK_GROUP_TEMPLATE = "Отлично! Теперь отправь мне название своей группы"

GROUP_DOESNT_EXISTS_TEMPLATE = "Такой группы нет!"


ASK_SURNAME_TEMPLATE = "Отправь свою фамилию"
ASK_NAME_TEMPLATE = "Отправь свое имя"

YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE = "Ваше заявление на регистрацию старостой было передано администраторам."
YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE = "Ваше заявление на регистрацию студентом было передано старосте."

ASK_BIRTHMONTH_TEMPLATE = """Введите номер месяца, в котором вы родились (1-12).
Это сделает бота еще удобнее для старосты. Если не хотите вводить свою дату рождения, то введите 0"""

ASK_BIRTHDAY_TEMPLATE = "Введите номер дня, в котором вы родились (1-31). Это сделает бота еще удобнее для старосты."
BIRTHMONTH_MUST_BE_DIGIT_TEMPLATE = "Номер месяца должен быть числом."
BIRTHMONTH_INCORRECT_TEMPLATE = "Номер месяца должен быть от 1 до 12 или 0."

BIRTHDAY_MUST_BE_DIGIT_TEMPLATE = "Номер дня должен быть числом."
BIRTHDAY_INCORRECT_TEMPLATE = "Неверная дата, введите снова."

GROUP_ALREADY_EXISTS_TEMPLATE = (
    "Данная группа уже существует. Может вы хотели добавить другую или зайти в существующую как студент?"
)

FAQ_TEMPLATE = """
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
# from asyncpg.pool import PoolConnectionProxy
#
# from src.dto import Lesson, Student
# from src.enums import VisitStatus
#
# __all__ = [
#     "HEADMAN_OR_STUDENT_MESSAGE",
#     "YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE",
#     "INCORRECT_DATA_MESSAGE",
#     "UNSUCCESFULLY_REG_MESSAGE",
#     "UNSUCCESFULL_STAROSTA_REG_MESSAGE",
#     "ALL_MESSAGE",
#     "NONE_MESSAGE",
#     "attendance_for_headmen_message",
#     "NO_LESSONS_TODAY",
#     "CHOOSE_PAIR_MESSAGE",
#     "POLL_MESSAGE",
#     "HEADMAN_SEND_MSG_MISTAKE",
#     "WHICH_PAIR_MESSAGE",
# ]
#
#
# HEADMAN_OR_STUDENT_MESSAGE = """
# Ты студент или староста?"""
#
# YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE = """
# Ваша группа еще не зарегестрирована.
# Для регистрации попросите вашего старосту зарегестрироваться в боте,
# после чего попробуйте снова"""
#
# INCORRECT_DATA_MESSAGE = """
# Данные введены неверно. Введите еще раз."""
#
#
# UNSUCCESFULLY_REG_MESSAGE = """
# Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова"""
#
#
# UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
# Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""
#
# WHICH_PAIR_MESSAGE = """
# Какая пара вас интересует?"""
#
#
# ALL_MESSAGE = """
# Вы посетите все пары"""
#
# NONE_MESSAGE = """
# Вы не посетите пары """
#
# NO_LESSONS_TODAY = """
# Сегодня нет пар!"""
#
# CHOOSE_PAIR_MESSAGE = """
# Выберите пару из списка:"""
#
# POLL_MESSAGE = """
# На какие сегодняшие пары ты придешь?
#
# Если возникли проблемы - напишите о них в @noheadproblemsbot"""
#
# HEADMAN_SEND_MSG_MISTAKE = """
# Произошла какая-то ошибка, и я не могу отправтить тебе информацию!"""
#
#
# async def attendance_for_headmen_message(lesson: Lesson, headman: Student, con: PoolConnectionProxy) -> str:
#     visit_text = "Придут:\n"
#     none_text = "Не отметились:\n"
#     no_text = "Не придут:\n"
#
#     not_visit: list[Student] = []
#     visit: list[Student] = []
#     not_checked: list[Student] = []
#
#     attendance_service = AttendanceService(con)
#     attendances = await attendance_service.get_visit_status_for_group_students(headman.group_id, lesson)
#
#     for student, visit_status in attendances.items():
#         match visit_status:
#             case VisitStatus.NOT_CHECKED:
#                 not_checked.append(student)
#             case VisitStatus.VISIT:
#                 visit.append(student)
#             case VisitStatus.NOT_VISIT:
#                 not_visit.append(student)
#
#     for student in sorted(not_checked, key=lambda student: student.fullname.lower()):
#         none_text += student.telegram_link
#
#     for student in sorted(visit, key=lambda student: student.fullname.lower()):
#         visit_text += student.telegram_link
#
#     for student in sorted(not_visit, key=lambda student: student.fullname.lower()):
#         no_text += student.telegram_link
#
#     return none_text + "\n" + visit_text + "\n" + no_text + "\n" + "Что-то еще?"
