from src.modules.university.api.contract import UniversityContract
from src.modules.university.api.dto import University
from src.modules.university.api.enums import UniversityAlias
from src.shared.services import PostgresService

__all__ = [
    "UniversityGateway",
]


class UniversityGateway(PostgresService):
    async def find_university_by_alias(self, alias: UniversityAlias) -> University:
        university_contract = UniversityContract(self._con)
        return await university_contract.find_university_by_alias(alias)
