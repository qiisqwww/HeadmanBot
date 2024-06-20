from enum import UNIQUE, StrEnum, verify

__all__ = [
    "CallbackData",
]


@verify(UNIQUE)
class CallbackData(StrEnum):
    START = "/start"
    RESTART = "Начать регистрацию заново"
    HELP = "Помощь"
    PROFILE = "Профиль"
    SHOW_SCHEDULE = "Узнать расписание"
    SHOW_ATTENDANCE = "Узнать посещаемость"
    ADMIN = "Админ панель"
    GROUP_PANEL = "Группа"
