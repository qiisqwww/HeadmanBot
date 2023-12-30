from enum import UNIQUE, StrEnum, verify

__all__ = [
    "TelegramCommand",
]


@verify(UNIQUE)
class TelegramCommand(StrEnum):
    START = "/start"
    HELP = "Помощь"
    GET_ATTENDANCE = "Узнать посещаемость"
    RESTART = "Начать регистрацию заново"
    PROFILE = "Профиль"

