from injector import inject

from src.modules.common.application import UseCase

from ...domain import Role
from ..repositories import StudentInfoRepository

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
