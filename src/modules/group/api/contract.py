from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.group.api.dto import GroupDTO
from src.modules.group.internal.services import GroupService
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "PostgresService",
]


class GroupContract(PostgresService):
    async def get_group_by_student(self, student: StudentDTO) -> GroupDTO:
        group_service = GroupService(self._con)
        return await group_service.get_by_student(student)

    async def append_student_into_group(self, student: StudentDTO, group: GroupDTO) -> None:
        group_service = GroupService(self._con)
        return await group_service.append_student_into_group(student, group)

    async def create_or_return_group(self, group_name: str, university_id: int) -> GroupDTO:
        group_service = GroupService(self._con)
        return await group_service.create_or_return(group_name, university_id)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        group_service = GroupService(self._con)
        return await group_service.find_by_name_and_uni(name, university_alias)

    async def get_students_id_by_group_name(self, group_name: str) -> list[int]:
        group_service = GroupService(self._con)
        return await group_service.get_stundents_id_by_group_name(group_name)
