from types import TracebackType
from typing import final

from asyncpg.transaction import Transaction
from injector import inject

from src.modules.common.application import UnitOfWork
from src.modules.common.infrastructure.database.database_connection import (
    DatabaseConnection,
)

__all__ = [
    "UnitOfWorkImpl",
]


@final
class UnitOfWorkImpl(UnitOfWork):
    _transaction: Transaction
    _con: DatabaseConnection

    @inject
    def __init__(self, con: DatabaseConnection) -> None:
        self._con = con

    async def __aenter__(self) -> None:
        self._transaction = await self._con.transaction()
        await self._transaction.start()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            await self._transaction.commit()
        else:
            await self._transaction.rollback()
