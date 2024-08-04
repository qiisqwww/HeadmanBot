from types import TracebackType
from typing import final

from asyncpg.transaction import Transaction
from injector import inject

from src.modules.common.application import UnitOfWork
from src.modules.common.infrastructure.database.database_connection import DbContext

__all__ = [
    "UnitOfWorkImpl",
]



@final
class UnitOfWorkImpl(UnitOfWork):
    _transaction: Transaction
    _ctx: DbContext

    @inject
    def __init__(self, ctx: DbContext) -> None:
        self._ctx = ctx

    async def __aenter__(self) -> None:
        self._transaction = await self._ctx.transaction()
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
