from pathlib import Path

from .env import BoolEnv, IntEnv, IntListEnv, StrEnv

__all__ = [
    "DEBUG",
    "BOT_TOKEN",
    "HEADMAN_PASSWORD",
    "LOGGING_PATH",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_PORT",
    "DB_HOST",
    "REDIS_HOST",
    "REDIS_PORT",
    "ADMIN_IDS",
]

DEBUG: bool = bool(BoolEnv("DEBUG"))
BOT_TOKEN: str = StrEnv("BOT_TOKEN")
HEADMAN_PASSWORD: str = StrEnv("HEADMAN_PASSWORD")
LOGGING_PATH: Path = Path(StrEnv("LOGGING_PATH"))


DB_USER: str = StrEnv("DB_USER")
DB_PASS: str = StrEnv("DB_PASS")
DB_NAME: str = StrEnv("DB_NAME")
DB_PORT: int = IntEnv("DB_PORT")
DB_HOST: str = StrEnv("DB_HOST")

REDIS_HOST: str = StrEnv("REDIS_HOST")
REDIS_PORT: int = IntEnv("REDIS_PORT")

ADMIN_IDS: list[int] = IntListEnv("ADMIN_IDS")
