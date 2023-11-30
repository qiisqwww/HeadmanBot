from src.modules.student.internal.services import StudentService
from src.shared.abstract_dto import AbstractStudent
from src.shared.services import PostgresService

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
