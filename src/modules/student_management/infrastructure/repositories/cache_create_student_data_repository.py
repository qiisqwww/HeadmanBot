from typing import Final, final

from src.modules.common.infrastructure.repositories import RedisRepositoryImpl
from src.modules.student_management.application.repositories import (
    CacheCreateStudentDataRepository,
    CreateStudentDTO,
)
from src.modules.student_management.infrastructure.mappers import CreateStudentDTOMapper

__all__ = [
    "CacheCreateStudentDataRepositoryImpl",
]


@final
class CacheCreateStudentDataRepositoryImpl(RedisRepositoryImpl, CacheCreateStudentDataRepository):
    _mapper: CreateStudentDTOMapper = CreateStudentDTOMapper()
    _SECONDS_TO_EXPIRE: Final[int] = 24 * 60 * 60 * 7  # 1 week

    async def cache(self, data: CreateStudentDTO) -> None:
        mapped_data = self._mapper.to_redis_dict(data)

        await self._con.hmset(mapped_data["telegram_id"], mapped_data)
        await self._con.expire(mapped_data["telegram_id"], self._SECONDS_TO_EXPIRE)

    async def fetch(self, telegram_id: int) -> CreateStudentDTO | None:
        record = await self._con.hgetall(str(telegram_id))
        if record:
            return self._mapper.from_redis_dict(record)
        return None

    async def delete(self, telegram_id: int) -> None:
        student_data = await self._con.hgetall(str(telegram_id))
        await self._con.hdel(str(telegram_id), *student_data)
