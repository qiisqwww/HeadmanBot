from datetime import date

from src.common.services import Service
from src.dto import Group, Student, StudentRaw, University
from src.enums import UniversityAlias

from .group_service import GroupService
from .student_service import StudentService
from .university_service import UniversityService

__all__ = [
    "AuthContractService",
]


class AuthContractService(Service):
    async def create_student(self, student_raw: StudentRaw) -> Student:
        student_service = StudentService(self._con)
        return await student_service.create(
            telegram_id=student_raw.telegram_id,
            name=student_raw.name,
            surname=student_raw.surname,
            birthday=student_raw.birthday,
            birthmonth=student_raw.birthmonth,
        )

    async def create_or_return_group(
        self, name: str, headman_id: int, university_id: int, payment_expired: date
    ) -> Group:
        group_service = GroupService(self._con)
        return await group_service.create_or_return(name, headman_id, university_id, payment_expired)

    async def append_student_into_group(self, group: Group, student: Student) -> None:
        group_service = GroupService(self._con)
        await group_service.append_student_into_group(group, student)

    async def find_group_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        group_service = GroupService(self._con)
        return await group_service.get_by_name_and_uni(name, university_alias)

    async def find_university_by_alias(self, university_alias: UniversityAlias) -> University:
        university_service = UniversityService(self._con)
        return await university_service.find_by_alias(university_alias)

    async def get_all_universities(self) -> list[University]:
        university_service = UniversityService(self._con)
        return await university_service.all()
