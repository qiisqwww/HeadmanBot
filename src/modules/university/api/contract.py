from src.kernel.base import PostgresService
from src.modules.university.api.dto import UniversityDTO
from src.modules.university.api.enums import UniversityAlias
from src.modules.university.internal.services import UniversityService

__all__ = [
    "UniversityService",
]


class UniversityContract(PostgresService):
    async def find_university_by_alias(self, alias: UniversityAlias) -> UniversityDTO:
        university_service = UniversityService(self._con)
        return await university_service.find_by_alias(alias)

    async def get_all_universities(self) -> list[UniversityDTO]:
        university_service = UniversityService(self._con)
        return await university_service.all()

    async def add_universities(self) -> None:
        university_service = UniversityService(self._con)
        return await university_service.add_universities()
