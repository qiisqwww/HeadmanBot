from types import TracebackType
from typing import final

from asyncpg.transaction import Transaction

from src.common.database.db_context import DbContext

__all__ = [
    "UnitOfWork",
]


@final
class UnitOfWork:
    _transaction: Transaction
    _ctx: DbContext

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
