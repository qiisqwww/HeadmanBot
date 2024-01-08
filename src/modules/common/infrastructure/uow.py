from types import TracebackType
from typing import final

from asyncpg.pool import PoolConnectionProxy
from asyncpg.transaction import Transaction
from injector import inject

from src.modules.common.application import UnitOfWork

__all__ = [
    "UnitOfWorkImpl",
]


@final
class UnitOfWorkImpl(UnitOfWork):
    _transaction: Transaction

    @inject
    def __init__(self, con: PoolConnectionProxy) -> None:
        self._transaction = con.transaction()

    async def __aenter__(self) -> None:
        await self._transaction.start()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if exc_type is None:
            await self._transaction.commit()
        else:
            await self._transaction.rollback()
