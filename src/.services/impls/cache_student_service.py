from datetime import date

from src.dto.models import StudentId, StudentLoginData
from src.services.interfaces import RedisService

__all__ = [
    "CacheStudentService",
]


class CacheStudentService(RedisService):
    async def cache_student(self, student_data: dict):
        birthdate: None | date = student_data["birthdate"]
        if birthdate is None:
            student_data["birthdate"] = "0"
        else:
            student_data["birthdate"] = str(birthdate)

        await self._con.hmset(student_data["telegram_id"], student_data)
        await self._con.expire(student_data["telegram_id"], 86400)

    async def pop_student_cache(self, student_id: StudentId) -> StudentLoginData:
        student_data = await self._con.hgetall(str(student_id))
        student_data["telegram_id"] = student_id

        await self._con.hdel(str(student_id), *student_data)

        if student_data["birthdate"] == "0":
            student_data["birthdate"] = None

        return StudentLoginData.from_mapping(student_data)