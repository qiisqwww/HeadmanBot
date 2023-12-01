from pathlib import Path

from .env import BoolEnv, IntListEnv, StrEnv

__all__ = [
    "DEBUG",
    "BOT_TOKEN",
    "LOGGING_PATH",
    "ADMIN_IDS",
]

DEBUG: bool = bool(BoolEnv("DEBUG"))
BOT_TOKEN: str = StrEnv("BOT_TOKEN")
LOGGING_PATH: Path = Path(StrEnv("LOGGING_PATH"))


ADMIN_IDS: list[int] = IntListEnv("ADMIN_IDS")
