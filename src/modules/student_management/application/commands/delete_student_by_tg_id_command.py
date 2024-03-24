from typing import final

from injector import inject

from src.modules.common.application import UseCase, UnitOfWork
from src.modules.student_management.application.exceptions import NotFoundStudentError
from src.modules.student_management.application.gateways import EduInfoModuleGateway, AttendanceModuleGateway
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums import Role

__all__ = [
    "DeleteStudentByTGIDCommand",
]


@final
class DeleteStudentByTGIDCommand(UseCase):
    _repository: StudentRepository
    _edu_info_module_gateway: EduInfoModuleGateway
    _attendance_module_gateway: AttendanceModuleGateway
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        repository: StudentRepository,
        edu_info_module_gateway: EduInfoModuleGateway,
        attendance_module_gateway: AttendanceModuleGateway,
        uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._edu_info_module_gateway = edu_info_module_gateway
        self._attendance_module_gateway = attendance_module_gateway
        self._uow = uow

    async def execute(self, telegram_id: int) -> None:
        async with self._uow:
            student = await self._repository.find_by_telegram_id(telegram_id)

            if student is None:
                raise NotFoundStudentError(
                    f"Not found student with telegram ID {telegram_id}",
                )

            if student.role == Role.HEADMAN:
                await self._edu_info_module_gateway.delete_group_by_id(student.group_id)
                await self._repository.delete_all_by_group_id(student.group_id)

                await self._attendance_module_gateway.delete_attendance_by_group_id(student.group_id)
                await self._attendance_module_gateway.delete_lessons_by_group_id(student.group_id)

                return

            await self._repository.delete_by_telegram_id(student.telegram_id)
            await self._attendance_module_gateway.delete_attendance_by_student_id(student.id)
