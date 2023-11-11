from asyncpg.pool import PoolConnectionProxy

__all__ = [
    "Repository",
]


class Repository:
    _con: PoolConnectionProxy

    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
