import sys

from loguru import logger

from .config import DEBUG, LOGGING_PATH

__all__ = [
    "configure_logger",
]


def configure_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
    )
    logger.add(
        LOGGING_PATH,
        level="INFO",
        compression="zip",
        rotation="500 MB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
    )
