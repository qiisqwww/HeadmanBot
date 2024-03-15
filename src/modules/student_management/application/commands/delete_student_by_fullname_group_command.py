from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.application.exceptions import (
    NotFoundStudentError,
    NotFoundGroupError
)
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain.enums import Role

__all__ = [
    "DeleteStudentByFullnameGroupCommand"
]


@final
class DeleteStudentByFullnameGroupCommand(UseCase):
    _repository: StudentRepository
    _gateway: EduInfoModuleGateway

    @inject
    def __init__(
            self,
            repository: StudentRepository,
            gateway: EduInfoModuleGateway
    ) -> None:
        self._repository = repository
        self._gateway = gateway

    async def execute(self, first_name: str, last_name: str, group_name: str) -> None:
        group = await self._gateway.find_group_by_name(group_name)

        if group is None:
            raise NotFoundGroupError(f"Not found group with name {group_name}")

        student = await self._repository.find_by_fullname_and_group_id(first_name, last_name, group.id)

        if student is None:
            raise NotFoundStudentError(f"Not found student with input data")

        if student.role == Role.HEADMAN:
            await self._gateway.delete_group_by_id(group.id)
            await self._repository.delete_all_by_group_id(group.id)

            return

        await self._repository.delete_by_fullname_and_group_id(first_name, last_name, group.id)
