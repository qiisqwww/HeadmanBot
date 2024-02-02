from pathlib import Path

from .env import BoolEnv, IntEnv, IntListEnv, StrEnv

__all__ = [
    "DEBUG",
    "BOT_TOKEN",
    "LOGGING_PATH",
    "ADMIN_IDS",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_PORT",
    "DB_HOST",
    "REDIS_HOST",
    "REDIS_PORT",
    "HTTP_PORT",
    "HTTP_HOST",
    "WEBHOOK_URL",
    "WEBHOOK_PATH",
    "WEBHOOK_SECRET",
    "THROTTLING_EXPIRE_TIME",
    "THROTTLING_RATE_PER_MINUTE"
]

DEBUG: bool = bool(BoolEnv("DEBUG"))
BOT_TOKEN: str = StrEnv("BOT_TOKEN")
LOGGING_PATH: Path = Path(StrEnv("LOGGING_PATH"))


ADMIN_IDS: list[int] = IntListEnv("ADMIN_IDS")


DB_USER: str = StrEnv("DB_USER")
DB_PASS: str = StrEnv("DB_PASS")
DB_NAME: str = StrEnv("DB_NAME")
DB_PORT: int = IntEnv("DB_PORT")
DB_HOST: str = StrEnv("DB_HOST")

REDIS_HOST: str = StrEnv("REDIS_HOST")
REDIS_PORT: int = IntEnv("REDIS_PORT")

HTTP_HOST: str = StrEnv("HTTP_HOST")
HTTP_PORT: int = IntEnv("HTTP_PORT")

WEBHOOK_PATH: str = StrEnv("WEBHOOK_PATH")
WEBHOOK_URL: str = StrEnv("WEBHOOK_URL")
WEBHOOK_SECRET: str = StrEnv("WEBHOOK_SECRET")

THROTTLING_EXPIRE_TIME: int = IntEnv("THROTTLING_EXPIRE_TIME")
THROTTLING_RATE_PER_MINUTE: int = IntEnv("THROTTLING_RATE_PER_MINUTE")
