from enum import StrEnum

__all__ = [
    "TelegramCommand",
]


class TelegramCommand(StrEnum):
    START = "/start"
    HELP = "Помощь"
    GET_ATTENDANCE = "Узнать посещаемость"
    RESTART = "Начать регистрацию заново"
