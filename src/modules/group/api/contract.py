from src.kernel.abstracts import AbstractStudent
from src.kernel.services import PostgresService
from src.modules.group.api.dto import Group
from src.modules.group.internal.services import GroupService
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "PostgresService",
]


class GroupContract(PostgresService):
    async def get_group_by_student(self, student: AbstractStudent) -> Group:
        group_service = GroupService(self._con)
        return await group_service.get_by_student(student)

    async def append_student_into_group(self, student: AbstractStudent, group: Group) -> None:
        group_service = GroupService(self._con)
        return await group_service.append_student_into_group(student, group)

    async def create_or_return_group(self, group_name: str, headman_id: int, university_id: int) -> Group:
        group_service = GroupService(self._con)
        return await group_service.create_or_return(group_name, headman_id, university_id)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        group_service = GroupService(self._con)
        return await group_service.find_by_name_and_uni(name, university_alias)
