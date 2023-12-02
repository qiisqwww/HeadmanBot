from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.group.api import GroupContract
from src.modules.group.api.dto import GroupDTO
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupGateway",
]


class GroupGateway(PostgresService):
    async def append_student_into_group(self, student: StudentDTO, group: GroupDTO) -> None:
        group_contract = GroupContract(self._con)
        return await group_contract.append_student_into_group(student, group)

    async def create_or_return_group(self, group_name: str, university_id: int) -> GroupDTO:
        group_contract = GroupContract(self._con)
        return await group_contract.create_or_return_group(group_name, university_id)

    async def find_group_by_name_and_uni(self, group_name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        group_contract = GroupContract(self._con)
        return await group_contract.find_by_name_and_uni(group_name, university_alias)

    async def get_students_id_by_group_name(self, group_name: str) -> list[int]:
        group_contract = GroupContract(self._con)
        return await group_contract.get_students_id_by_group_name(group_name)
