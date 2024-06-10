from injector import inject

from src.modules.common.infrastructure.database import DatabaseConnection

__all__ = [
    "PostgresRepositoryImpl",
]


class PostgresRepositoryImpl:
    _con: DatabaseConnection

    @inject
    def __init__(self, con: DatabaseConnection) -> None:
        self._con = con
