from types import TracebackType
from typing import TYPE_CHECKING, TypeAlias, final

from asyncpg.pool import PoolConnectionProxy
from asyncpg.transaction import Transaction
from injector import inject

from src.modules.common.application import UnitOfWork

__all__ = [
    "UnitOfWorkImpl",
]

if TYPE_CHECKING:
    from asyncpg import Record
    DatabaseConnection: TypeAlias = PoolConnectionProxy[Record]
else:
    DatabaseConnection: TypeAlias = PoolConnectionProxy

@final
class UnitOfWorkImpl(UnitOfWork):
    _transaction: Transaction

    @inject
    def __init__(self, con: DatabaseConnection) -> None:
        self._transaction = con.transaction()

    async def __aenter__(self) -> None:
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
