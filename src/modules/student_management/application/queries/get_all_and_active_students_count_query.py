from injector import inject

from src.modules.common.application import UseCase

from ..repositories import StudentRepository

__all__ = [
    "GetAllAndActiveStudentsCountQuery",
]


class GetAllAndActiveStudentsCountQuery(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[int]:  # ALWAYS returns a list only of 2 numbers
        return [await self._repository.get_students_count(), await self._repository.get_active_students_count()]
