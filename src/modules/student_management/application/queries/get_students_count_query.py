from injector import inject

from src.modules.common.application import UseCase

from ..repositories import StudentRepository

__all__ = [
    "GetStudentsCountQuery",
]


class GetStudentsCountQuery(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[int]:
        return [await self._repository.get_students_count(), await self._repository.get_active_students_count()]
