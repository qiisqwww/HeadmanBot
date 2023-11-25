from loguru import logger

from .config import DEBUG, LOGGING_PATH

__all__ = [
    "configurate_logger",
]


def configurate_logger() -> None:
    logger.add(
        LOGGING_PATH,
        compression="zip",
        rotation="500 MB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
    )
