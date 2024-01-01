from src.application.edu_info.repositories import UniversityRepository
from src.domain.edu_info import University

__all__ = [
    "GetAllUniversitiesQuery",
]


class GetAllUniversitiesQuery:
    _repository: UniversityRepository

    def __init__(self, repository: UniversityRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[University]:
        return await self._repository.all()
