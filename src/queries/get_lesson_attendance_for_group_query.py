from injector import inject

from src.common import UseCase
from src.modules.attendance.application.gateways import StudentManagementGateway
from src.modules.attendance.application.repositories import GroupAttendanceRepository
from src.modules.attendance.domain import LessonAttendanceForGroup

__all__ = [
    "GetLessonAttendanceForGroupQuery",
]


class GetLessonAttendanceForGroupQuery(UseCase):
    _gateway: StudentManagementGateway
    _repository: GroupAttendanceRepository

    @inject
    def __init__(self, gateway: StudentManagementGateway, repository: GroupAttendanceRepository) -> None:
        self._gateway = gateway
        self._repository = repository

    async def execute(self, group_id: int, lesson_id: int) -> LessonAttendanceForGroup:
        students_info = await self._gateway.filter_student_info_by_group_id(group_id)
        return await self._repository.find_group_visit_status_for_lesson(group_id, lesson_id, students_info)
