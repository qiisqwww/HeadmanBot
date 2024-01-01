from src.domain.student_management import Student

from ..repositories import StudentRepository

__all__ = [
    "FindStudentQuery",
]


class FindStudentQuery:
    _repository: StudentRepository

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self, telegram_id: int) -> Student | None:
        return await self._repository.find_by_id(telegram_id)
