from typing import final

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.exceptions import NotFoundStudentError
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums import Role

__all__ = [
    "DeleteStudentByTGIDCommand",
]


@final
class DeleteStudentByTGIDCommand(UseCase):
    _repository: StudentRepository
    _gateway: EduInfoModuleGateway

    @inject
    def __init__(
        self,
        repository: StudentRepository,
        gateway: EduInfoModuleGateway,
    ) -> None:
        self._repository = repository
        self._gateway = gateway

    async def execute(self, telegram_id: int) -> None:
        student = await self._repository.find_by_telegram_id(telegram_id)

        if student is None:
            raise NotFoundStudentError(
                f"Not found student with telegram ID {telegram_id}",
            )

        if student.role == Role.HEADMAN:
            await self._gateway.delete_group_by_id(student.group_id)
            await self._repository.delete_all_by_group_id(student.group_id)

            return

        await self._repository.delete_by_telegram_id(telegram_id)
