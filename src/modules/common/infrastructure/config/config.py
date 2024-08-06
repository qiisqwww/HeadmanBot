from pathlib import Path  # noqa: EXE002

from src.modules.common.infrastructure.config import env

from .env import Env, EnvList

__all__ = [
    "DEBUG",
    "BOT_TOKEN",
    "SQL_LOGGING_PATH",
    "INFO_LOGGING_PATH",
    "ERROR_LOGGING_PATH",
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
    "THROTTLING_RATE_PER_MINUTE",
    "UVICORN_WORKERS_COUNT",
    "CELERY_BROKER_URL",
    "CELERY_RESULT_BACKEND",
]

TESTING = Env("TESTING", bool)
env.CAN_USE_DEFAULT_VALUE = TESTING

DEBUG = Env("DEBUG", bool, True)
BOT_TOKEN = Env("BOT_TOKEN", str, "")

SQL_LOGGING_PATH = Env("SQL_LOGGING_PATH", Path, Path("logs/sql.log"))
INFO_LOGGING_PATH = Env("INFO_LOGGING_PATH", Path, Path("logs/info.log"))
ERROR_LOGGING_PATH = Env("ERROR_LOGGING_PATH", Path, Path("logs/error.log"))

ADMIN_IDS = EnvList("ADMIN_IDS", int, [])

DB_USER = Env("DB_USER", str, "root")
DB_PASS = Env("DB_PASS", str, "root1234")
DB_NAME = Env("DB_NAME", str, "root")
DB_PORT = Env("DB_PORT", str, 5432)
DB_HOST = Env("DB_HOST", str, "postgres")

REDIS_HOST = Env("REDIS_HOST", str, "redis")
REDIS_PORT = Env("REDIS_PORT", int, 6379)

HTTP_HOST = Env("HTTP_HOST", str, "0.0.0.0")
HTTP_PORT = Env("HTTP_PORT", int, 8000)
UVICORN_WORKERS_COUNT = Env("UVICORN_WORKERS_COUNT", int, 1)

WEBHOOK_PATH = Env("WEBHOOK_PATH", str, "/webhook")
WEBHOOK_URL = Env("WEBHOOK_URL", str, "")
WEBHOOK_SECRET = Env("WEBHOOK_SECRET", str, "fdglhkjfpsdflgkjhlfkdsf;gkjdl")

THROTTLING_RATE_PER_MINUTE = Env("THROTTLING_RATE_PER_MINUTE", int, 1_000_000)

CELERY_BROKER_URL = Env("CELERY_BROKER_URL", str, "redis://redis:6379/0")
CELERY_RESULT_BACKEND = Env("CELERY_RESULT_BACKEND", str, "redis://redis:6379/0")
