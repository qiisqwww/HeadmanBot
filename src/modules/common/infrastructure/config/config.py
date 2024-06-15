from pathlib import Path  # noqa: EXE002

from .env import Env, EnvList

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
    "THROTTLING_RATE_PER_MINUTE",
    "UVICORN_WORKERS_COUNT",
]

DEBUG = Env("DEBUG", bool)
BOT_TOKEN = Env("BOT_TOKEN", str)
LOGGING_PATH = Env("LOGGING_PATH", Path)


ADMIN_IDS = EnvList("ADMIN_IDS", int)


DB_USER = Env("DB_USER", str)
DB_PASS = Env("DB_PASS", str)
DB_NAME = Env("DB_NAME", str)
DB_PORT = Env("DB_PORT", str)
DB_HOST = Env("DB_HOST", str)

REDIS_HOST = Env("REDIS_HOST", str)
REDIS_PORT = Env("REDIS_PORT", int)

HTTP_HOST = Env("HTTP_HOST", str)
HTTP_PORT = Env("HTTP_PORT", int)
UVICORN_WORKERS_COUNT = Env("UVICORN_WORKERS_COUNT", int)

WEBHOOK_PATH = Env("WEBHOOK_PATH", str)
WEBHOOK_URL = Env("WEBHOOK_URL", str)
WEBHOOK_SECRET = Env("WEBHOOK_SECRET", str)

THROTTLING_RATE_PER_MINUTE = Env("THROTTLING_RATE_PER_MINUTE", int)
