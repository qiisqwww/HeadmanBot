from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "ChangeAdminGroupCommand",
]


class ChangeAdminGroupCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int, group_id: int) -> None:
        await self._repository.change_admin_group_by_telegram_id(telegram_id, group_id)
