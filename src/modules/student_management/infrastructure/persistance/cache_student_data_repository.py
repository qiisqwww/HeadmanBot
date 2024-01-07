from typing import Final, final

from src.modules.common.infrastructure.persistence.redis_repository import (
    RedisRepositoryImpl,
)
from src.modules.student_management.application.repositories import (
    CacheStudentDataRepository,
    CreateStudentDTO,
)
from src.modules.student_management.infrastructure.mappers import CreateStudentDTOMapper

__all__ = [
    "CacheStudentDataRepositoryImpl",
]


@final
class CacheStudentDataRepositoryImpl(RedisRepositoryImpl, CacheStudentDataRepository):
    _mapper: CreateStudentDTOMapper = CreateStudentDTOMapper()
    _SECONDS_TO_EXPIRE: Final[int] = 24 * 60 * 60  # 24 hours

    async def cache(self, data: CreateStudentDTO) -> None:
        mapped_data = self._mapper.to_redis_dict(data)

        await self._con.hmset(mapped_data["telegram_id"], mapped_data)
        await self._con.expire(mapped_data["telegram_id"], self._SECONDS_TO_EXPIRE)

    async def pop(self, telegram_id: int) -> CreateStudentDTO:
        student_data = await self._con.hgetall(str(telegram_id))
        await self._con.hdel(str(telegram_id), *student_data)

        return self._mapper.from_redis_dict(student_data)
