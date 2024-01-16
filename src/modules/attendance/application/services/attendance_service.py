from src.dto.models import LessonId, StudentId
from src.enums import VisitStatus
from src.repositories import AttendanceRepository
from src.services.interfaces import AttendanceService, LessonService, StudentService

__all__ = [
    "AttendanceServiceImpl",
]


class AttendanceServiceImpl(AttendanceService):
    _lesson_service: LessonService
    _attendance_repository: AttendanceRepository
    _student_service: StudentService

    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        lesson_service: LessonService,
        student_service: StudentService,
    ) -> None:
        self._attendance_repository = attendance_repository
        self._lesson_service = lesson_service
        self._student_service = student_service

    async def recreate_attendances(self) -> None:
        await self._attendance_repository.delete_all_attendances()

        students = await self._student_service.all()
        for student in students:
            await self.create_for_student(student)

    async def update_visit_status_all(self, student_id: StudentId, new_status: VisitStatus) -> None:
        await self._attendance_repository.update_visit_status_all(student_id, new_status)

    async def update_visit_status_for_lesson(
        self, student_id: StudentId, lesson_id: LessonId, new_status: VisitStatus
    ) -> None:
        attendances = await self.filter_by_student_id(student_id)

        for attendance in attendances:
            if attendance.status == VisitStatus.NOT_CHECKED:
                await self._attendance_repository.update_status_for_lesson(
                    student_id, attendance.lesson.id, VisitStatus.NOT_VISIT
                )

        await self._attendance_repository.update_status_for_lesson(student_id, lesson_id, new_status)
