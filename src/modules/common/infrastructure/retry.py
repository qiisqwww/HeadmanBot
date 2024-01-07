from collections.abc import Callable

__all__ = [
    "retry",
]


def retry(attempts: int = 1) -> Callable:
    def retry_decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise e

        return wrapper

    return retry_decorator
