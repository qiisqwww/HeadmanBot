from pathlib import Path

from src.modules.common.domain import UniversityAlias

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

UNIVERSITIES_LIST: list[tuple[str, UniversityAlias]] = [
    ("РТУ МИРЭА", UniversityAlias.MIREA),
    ("МГТУ им. Н.Э. Баумана", UniversityAlias.BMSTU),
]
