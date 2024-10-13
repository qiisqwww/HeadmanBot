import sys
from collections.abc import Callable, Mapping
from typing import Any

import logging
from loguru import logger

from .config import DEBUG, ERROR_LOGGING_PATH, INFO_LOGGING_PATH, SQL_LOGGING_PATH

__all__ = [
    "configure_logger",
]



def level_filter(level: str) -> Callable[[Mapping[str, Any]], bool]:
    def is_level(record: Mapping[str, Any]) -> bool:
        return record["level"].name == level
    return is_level


def configure_logger() -> None:
    logger.remove()
    logger.level("SQL", no=5, color="green", icon="SQL")

    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
    )

    logger.add(
        INFO_LOGGING_PATH,
        level="INFO",
        compression="zip",
        rotation="1 GB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
        serialize=True,
        filter=level_filter("INFO"),
    )

    logger.add(
        SQL_LOGGING_PATH,
        level="SQL",
        compression="zip",
        rotation="1 GB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
        serialize=True,
        filter=level_filter("SQL"),
    )

    logger.add(
        ERROR_LOGGING_PATH,
        level="ERROR",
        compression="zip",
        rotation="1 GB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
        serialize=True,
        filter=level_filter("ERROR"),
    )

    # Celery logging

    logging.basicConfig(filename="logs/logging-info.log", level=logging.INFO)
    logging.basicConfig(filename="logs/logging-error.log", level=logging.ERROR)
