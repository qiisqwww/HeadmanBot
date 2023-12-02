from src.kernel.base import RedisService
from src.modules.student.internal.dto import StudentRawDTO

__all__ = [
    "CacheStudentService",
]


class CacheStudentService(RedisService):
    async def cache_student(self, student_data: dict):
        if student_data["birthdate"] is None:
            student_data["birthdate"] = "0"

        await self._con.hmset(student_data["telegram_id"], student_data)
        await self._con.expire(student_data["telegram_id"], 86400)

    async def pop_student_cache(self, student_id: int) -> StudentRawDTO:
        student_data = await self._con.hgetall(str(student_id))
        student_data["telegram_id"] = student_id

        await self._con.hdel(str(student_id), *student_data)

        if student_data["birthdate"] == "0":
            student_data["birthdate"] = None

        return StudentRawDTO.from_mapping(student_data)
