from collections.abc import Callable, Coroutine
from typing import Any, TypeAlias, TypeVar

from aiohttp import ClientError

__all__ = [
    "aiohttp_retry",
]


T = TypeVar("T")
DecoratedCallable: TypeAlias = Callable[..., Coroutine[Any, Any, T]]


def aiohttp_retry(attempts: int = 1) -> Callable[[DecoratedCallable[T]], DecoratedCallable[T]]:
    def retry_decorator(func: DecoratedCallable[T]) -> DecoratedCallable[T]:
        async def wrapper(*args: Any) -> T: # noqa: ANN401
            i = 0
            while True:
                try:
                    return await func(*args)
                except (ClientError, TimeoutError) as e:
                    if i == attempts - 1:
                        raise e # noqa: TRY201

                i += 1

        return wrapper

    return retry_decorator
