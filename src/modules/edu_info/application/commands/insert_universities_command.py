from typing import Final

from src.modules.common.domain import UniversityAlias

from ..repositories import UniversityRepository

__all__ = [
    "InsertUniversitiesCommand",
]


class InsertUniversitiesCommand:
    _repository: Final[UniversityRepository]
    _UNIVERSITIES_LIST: tuple[tuple[str, UniversityAlias], ...] = (
        ("РТУ МИРЭА", UniversityAlias.MIREA),
        ("МГТУ им. Н.Э. Баумана", UniversityAlias.BMSTU),
    )

    def __init__(self, repository: UniversityRepository) -> None:
        self._repository = repository

    async def execute(self) -> None:
        for uni_data in self._UNIVERSITIES_LIST:
            uni = await self._repository.find_by_name(uni_data[0])

            if uni is None:
                await self._repository.create(*uni_data)
