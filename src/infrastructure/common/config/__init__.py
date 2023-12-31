from .config import (
    ADMIN_IDS,
    BOT_TOKEN,
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
    LOGGING_PATH,
    REDIS_HOST,
    REDIS_PORT,
    UNIVERSITIES_LIST,
)
from .logger_config import configurate_logger

__all__ = [
    "BOT_TOKEN",
    "DEBUG",
    "LOGGING_PATH",
    "ADMIN_IDS",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_PORT",
    "DB_HOST",
    "REDIS_PORT",
    "REDIS_HOST",
    "configurate_logger",
    "UNIVERSITIES_LIST",
]
