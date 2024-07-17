from typing import final

from injector import inject

from src.modules.common.application import UseCase, UnitOfWork

from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums.role import Role

__all__ = [
    "ExpelUserFromGroupCommand",
]


@final
class ExpelUserFromGroupCommand(UseCase):
    _repository: StudentRepository
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        repository: StudentRepository,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self,
        student_id: int,
    ) -> None:
        async with self._uow:
            await self._repository.expel_user_from_group_by_id(student_id)
            await self._repository.set_role_by_id(student_id, Role.IS_REGISTERED)
