from aiogram.filters import Filter
from aiogram.types import Message

from .telegram_command import TelegramCommand

__all__ = [
    "CommandFilter",
]


class CommandFilter(Filter):
    _command: TelegramCommand

    def __init__(self, command: TelegramCommand) -> None:
        self._command = command

    async def __call__(self, message: Message) -> bool:
        return message.text == self._command
