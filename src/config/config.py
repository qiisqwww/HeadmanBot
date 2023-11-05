from pathlib import Path

from .env import BoolEnv, StrEnv

__all__ = [
    "DEBUG",
    "BOT_TOKEN",
    "HEADMAN_PASSWORD",
    "DB_PATH",
    "LOGGING_PATH",
]

DEBUG: bool = bool(BoolEnv("DEBUG"))
BOT_TOKEN: str = StrEnv("BOT_TOKEN")
HEADMAN_PASSWORD: str = StrEnv("HEADMAN_PASSWORD")
DB_PATH: str = StrEnv("DB_PATH")
LOGGING_PATH = Path("logs/logs.log")
