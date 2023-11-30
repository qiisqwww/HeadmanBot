from src.modules.university.api import UniversityContract
from src.modules.university.api.dto import University
from src.modules.university.api.enums import UniversityAlias
from src.shared.services import PostgresService

__all__ = [
    "UniversityGatewate",
]


class UniversityGatewate(PostgresService):
    async def find_university_by_alias(self, alias: UniversityAlias) -> University:
        university_contract = UniversityContract(self._con)
        return await university_contract.find_university_by_alias(alias)

    async def get_all_universities(self) -> list[University]:
        university_contract = UniversityContract(self._con)
        return await university_contract.get_all_universities()
