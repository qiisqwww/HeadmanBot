from typing import final

from aiogram.filters import BaseFilter
from aiogram.types import Message

from .telegram_command import TelegramCommand

__all__ = [
    "CommandFilter",
]


@final
class CommandFilter(BaseFilter): # type: ignore [misc]
    _command: TelegramCommand

    def __init__(self, command: TelegramCommand) -> None:
        self._command = command

    async def __call__(self, message: Message) -> bool:
        return bool(message.text == str(self._command))
