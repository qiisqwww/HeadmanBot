from src.dto.models import GroupId, LessonId, Student, StudentId, StudentReadFullname
from src.dto.models.attendance_with_lesson import AttendanceWithLesson
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

    async def get_visit_status_for_group_students(
        self, group_id: GroupId, lesson_id: LessonId
    ) -> dict[StudentReadFullname, VisitStatus]:
        return await self._attendance_repository.get_visit_status_for_group_students(group_id, lesson_id)

    async def get_visit_status_by_student_id_and_lesson(
        self, student_id: StudentId, lesson_id: LessonId
    ) -> VisitStatus:
        return await self._attendance_repository.get_visit_status_by_student_id_and_lesson(student_id, lesson_id)

    async def update_visit_status_all(self, student_id: StudentId, new_status: VisitStatus) -> None:
        await self._attendance_repository.update_visit_status_all(student_id, new_status)

    async def filter_by_student_id(self, student_id: StudentId) -> list[AttendanceWithLesson]:
        return await self._attendance_repository.filter_by_student_id(student_id)

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

    async def create_for_student(self, student: Student) -> None:
        lessons = await self._lesson_service.filter_by_group_id(student.group_id)

        if not lessons:
            return

        await self._attendance_repository.create(student.telegram_id, [lesson.id for lesson in lessons])
