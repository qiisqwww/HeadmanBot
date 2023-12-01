from src.kernel.abstracts import AbstractStudent
from src.kernel.services import PostgresService
from src.modules.group.api import GroupContract
from src.modules.group.api.dto import Group
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupGateway",
]


class GroupGateway(PostgresService):
    async def get_headman_id(self, student: AbstractStudent) -> int:
        group_contract = GroupContract(self._con)
        group = await group_contract.get_group_by_student(student)

        return group.headman_id

    async def append_student_into_group(self, student: AbstractStudent, group: Group) -> None:
        group_contract = GroupContract(self._con)
        return await group_contract.append_student_into_group(student, group)

    async def create_or_return_group(self, group_name: str, headman_id: int, university_id: int) -> Group:
        group_contract = GroupContract(self._con)
        return await group_contract.create_or_return_group(group_name, headman_id, university_id)

    async def find_group_by_name_and_uni(self, group_name: str, university_alias: UniversityAlias) -> Group | None:
        group_contract = GroupContract(self._con)
        return await group_contract.find_by_name_and_uni(group_name, university_alias)
