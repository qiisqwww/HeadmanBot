from enum import UNIQUE, StrEnum, verify

__all__ = [
    "TelegramCommand",
]


@verify(UNIQUE)
class TelegramCommand(StrEnum):
    START = "/start"
    RESTART = "Начать регистрацию заново"
    HELP = "Помощь"
    PROFILE = "Профиль"
    SHOW_GROUP_ATTENDANCE = "Узнать посещаемость"
