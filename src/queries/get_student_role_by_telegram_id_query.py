from injector import inject

from src.common import UseCase
from src.modules.student_management.application.repositories import StudentInfoRepository
from src.modules.student_management.domain import Role

__all__ = [
    "GetStudentRoleByTelegramIDQuery",
]


class GetStudentRoleByTelegramIDQuery(UseCase):
    _repository: StudentInfoRepository

    @inject
    def __init__(self, repository: StudentInfoRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> Role:
        return await self._repository.get_role_by_telegram_id(telegram_id)
