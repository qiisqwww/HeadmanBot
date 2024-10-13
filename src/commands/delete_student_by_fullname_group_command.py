from typing import final

from injector import inject
from src.modules.student_management.application.gateways import AttendanceModuleGateway, EduInfoModuleGateway
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums import Role

from src.common import UnitOfWork, UseCase
from src.common.exceptions import NotFoundGroupError, NotFoundStudentError

__all__ = [
    "DeleteStudentByFullnameGroupCommand",
]


@final
class DeleteStudentByFullnameGroupCommand(UseCase):
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
            uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._edu_info_module_gateway = edu_info_module_gateway
        self._attendance_module_gateway = attendance_module_gateway
        self._uow = uow

    async def execute(self, first_name: str, last_name: str, group_name: str) -> None:
        async with self._uow:
            group = await self._edu_info_module_gateway.find_group_by_name(group_name)

            if group is None:
                msg = f"Not found group with name {group_name}"
                raise NotFoundGroupError(msg)

            student = await self._repository.find_by_fullname_and_group_id(first_name, last_name, group.id)

            if student is None:
                msg = "Not found student with input data"
                raise NotFoundStudentError(msg)

            if student.role == Role.HEADMAN:
                await self._edu_info_module_gateway.delete_group_by_id(group.id)
                await self._repository.delete_all_by_group_id(group.id)

                await self._attendance_module_gateway.delete_attendance_by_group_id(student.group_id)
                await self._attendance_module_gateway.delete_lessons_by_group_id(student.group_id)

                return

            await self._repository.delete_by_fullname_and_group_id(student.first_name, student.last_name, group.id)
            await self._attendance_module_gateway.delete_attendance_by_student_id(student.id)
