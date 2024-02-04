from collections.abc import Callable, Coroutine
from typing import Any, TypeAlias

from aiohttp import ClientError, ClientResponse

__all__ = [
    "aiohttp_retry",
]



DecoratedCallable: TypeAlias = Callable[..., Coroutine[Any, Any, ClientResponse]]


def aiohttp_retry(attempts: int = 1) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def retry_decorator(func: DecoratedCallable) -> DecoratedCallable:
        async def wrapper(*args: Any) -> ClientResponse: # noqa: ANN401
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
