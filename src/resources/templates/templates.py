from src.enums import Role

__all__ = [
    "start_message_template",
    "CHOOSE_STUDENT_ROLE_TEMPLATE",
    "REGISTRATION_DENIED_TEMPLATE",
    "REGISTRATION_ACCEPTED_TEMPLATE",
    "YOU_WERE_DENIED_TEMPLATE",
    "YOU_WERE_ACCEPTED_TEMPLATE",
    "ASK_UNIVERSITY_TEMPLATE",
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
    "FAQ_TEMPLATE",
    "GROUP_DOESNT_REGISTERED_TEMPLATE",
    "BIRTHDATE_INCORRECT_TEMPLATE",
    "ASK_BIRTHDATE_TEMPLATE"
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


def successful_role_choose_template(role: Role) -> str:
    return f"Роль была успешно выбрана. Вы - <b>{role}</b>."


def successful_university_choose_template(university_name: str) -> str:
    return f"Вы успешно выбрали университет <b>{university_name}</b>."


ASK_GROUP_TEMPLATE = "Отправь название своей группы"

GROUP_DOESNT_EXISTS_TEMPLATE = "В выбранном университете такой группы нет"

ASK_SURNAME_TEMPLATE = "Отправь свою фамилию"

ASK_NAME_TEMPLATE = "Отправь свое имя"

YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE = "Ваше заявление на регистрацию старостой было передано администраторам."

YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE = "Ваше заявление на регистрацию студентом было передано старосте."

ASK_BIRTHDATE_TEMPLATE = """Введите дату рождения в формате ДД.ММ.ГГГГ.
Это поможет сделать бота еще удобнее. 
Если вы не хотите указывать свою дату рождения, введите 0"""

BIRTHDATE_INCORRECT_TEMPLATE = "Вы ввели некорректные данные. Введите дату в формате ДД.ММ.ГГГГ"

HEADMAN_ALREADY_EXISTS_TEMPLATE = "У выбранной группы уже есть староста."

FAQ_TEMPLATE = """
<b>Grand Headman MIREA был разработан как инструмент-помощник для старост.</b>


Каждый учебный день, в 07:00, бот рассылает студентам сообщение с опросом. В нем студент должен отметить,
на каких парах он обещает присутствовать. 

<b>Доступно несколько вариантов ответа:</b>
1. Студент отмечает, что придет на все пары.
2. Студент отмечает, что сегодня его в университете не будет
3. Студент указывает конкретные пары, которые он обещает посетить. На все остальные пары он автоматически будет записан, 
как отсутствующий.

<b>Опрос ограничен по времени.</b> Отметиться можно с в промежутке между 7 утра и концом первой <b>(по счету)</b>
 пары вашей группы.

Старосте допуступна команда <b>Узнать посещаемость</b>, с помощью которой он может получить информацию о 
посещаемости группы на текущий момент.

<b>ВНИМАНИЕ!!!</b> Бот находится на стадии разработки, потому, к сожалению, пероидически могут возникать неполадки.
Если есть вопросы или предложения - вы можете написать их <b>сюда --->>> @noheadproblemsbot</b>
Благодарим за понимание
"""

GROUP_DOESNT_REGISTERED_TEMPLATE = "Группа не зарегистрированна в боте, попросите свою старосту ее зерегистрировать."
