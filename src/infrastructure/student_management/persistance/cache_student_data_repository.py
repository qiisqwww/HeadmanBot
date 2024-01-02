from typing import Final

from src.application.student_management.repositories import (
    CacheStudentDataRepository,
    CreateStudentDTO,
)
from src.infrastructure.common.persistence import RedisRepositoryImpl
from src.infrastructure.student_management.mappers import CreateStudentDTOMapper

__all__ = [
    "CacheStudentDataRepositoryImpl",
]


class CacheStudentDataRepositoryImpl(RedisRepositoryImpl, CacheStudentDataRepository):
    _mapper: CreateStudentDTOMapper = CreateStudentDTOMapper()
    _SECONDS_TO_EXPIRE: Final[int] = 24 * 60 * 60  # 24 hours

    async def cache(self, data: CreateStudentDTO) -> None:
        mapped_data = self._mapper.to_redis_dict(data)

        await self._con.hmset(mapped_data["telegram_id"], mapped_data)
        await self._con.expire(mapped_data["telegram_id"], self._SECONDS_TO_EXPIRE)

    async def pop(self, student_id: int) -> CreateStudentDTO:
        student_data = await self._con.hgetall(str(student_id))
        await self._con.hdel(str(student_id), *student_data)

        return self._mapper.from_redis_dict(student_data)
