from src.common.services import RedisService
from src.dto import StudentRaw

__all__ = [
    "CacheStudentService",
]


class CacheStudentService(RedisService):
    async def cache_student(self, student_data: dict):
        await self._con.hmset(student_data["telegram_id"], student_data)
        await self._con.expire(student_data["telegram_id"], 86400)

    async def pop_student_cache(self, student_id: int) -> StudentRaw:
        student_data = await self._con.hgetall(str(student_id))
        student_data["telegram_id"] = student_id

        await self._con.hdel(str(student_id), *student_data)

        return StudentRaw.from_mapping(student_data)
