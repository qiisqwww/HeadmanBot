from src.domain.student_management import Student

from ..repositories import StudentRepository

__all__ = [
    "FindStudentQuery",
]


class FindStudentQuery:
    _telegram_id: int
    _repository: StudentRepository

    def __init__(self, telegram_id: int, repository: StudentRepository) -> None:
        self._telegram_id = telegram_id
        self._repository = repository

    async def execute(self) -> Student | None:
        return await self._repository.find_by_id(self._telegram_id)
