from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.student.internal.services import StudentService

__all__ = [
    "FindStudentContract",
]


class FindStudentContract(PostgresService):
    async def find_student(self, telegram_id: int) -> StudentDTO | None:
        student_service = StudentService(self._con)
        return await student_service.find(telegram_id)
