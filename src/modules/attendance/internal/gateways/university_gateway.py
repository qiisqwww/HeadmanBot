from src.kernel.base import PostgresService
from src.modules.group.api.dto.group_dto import GroupDTO
from src.modules.university.api.contract import UniversityContract
from src.modules.university.api.dto import UniversityDTO

__all__ = [
    "UniversityGateway",
]


class UniversityGateway(PostgresService):
    async def get_university_by_group(self, group: GroupDTO) -> UniversityDTO:
        university_contract = UniversityContract(self._con)
        return await university_contract.get_university_by_group(group)
