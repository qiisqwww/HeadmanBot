from src.common.database import DbContext

__all__ = [
    "PostgresRepository",
]


class PostgresRepository:
    _con: DbContext

    def __init__(self, con: DbContext) -> None:
        self._con = con
