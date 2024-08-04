from injector import inject

from src.modules.common.infrastructure.database import DbContext

__all__ = [
    "PostgresRepositoryImpl",
]


class PostgresRepositoryImpl:
    _con: DbContext

    @inject
    def __init__(self, con: DbContext) -> None:
        self._con = con
