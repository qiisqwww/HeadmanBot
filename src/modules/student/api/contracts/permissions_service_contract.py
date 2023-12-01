from src.kernel.abstracts import AbstractStudent
from src.kernel.services import PostgresService
from src.modules.student.internal.services import StudentService

__all__ = [
    "PermissionsServiceContract",
]


class PermissionsServiceContract(PostgresService):
    async def check_is_student_registered_and_return(self, telegram_id: int) -> AbstractStudent | None:
        student_service = StudentService(self._con)
        return await student_service.find(telegram_id)

    async def check_is_headman(self, student: AbstractStudent) -> bool:
        student_service = StudentService(self._con)
        return await student_service.is_headman(student)
