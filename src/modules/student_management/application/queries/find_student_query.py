from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain import Student

__all__ = [
    "FindStudentByTelegramIdQuery",
]


class FindStudentByTelegramIdQuery(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> Student | None:
        return await self._repository.find_by_telegram_id(telegram_id)
