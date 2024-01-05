from ..repositories import CacheStudentDataRepository

__all__ = [
    "ClearCreateStudentDataCacheCommand",
]


class ClearCreateStudentDataCacheCommand:
    _repository: CacheStudentDataRepository

    def __init__(self, repository: CacheStudentDataRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> None:
        await self._repository.pop(telegram_id)
