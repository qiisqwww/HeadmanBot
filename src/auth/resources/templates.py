__all__ = [
    "start_message_template",
    "CHOOSE_STUDENT_ROLE_TEMPLATE",
]


def start_message_template(surname: str | None, name: str) -> str:
    if surname is None:
        return f"Приветствую {name}! Для начала, давай зарегестрируемся в системе бота."
    return f"Приветствую {surname} {name}! Для начала, давай зарегестрируемся в системе бота."


CHOOSE_STUDENT_ROLE_TEMPLATE = "Нажмите на кнопку 'Я студент' или 'Я староста', чтобы выбрать свою роль."
