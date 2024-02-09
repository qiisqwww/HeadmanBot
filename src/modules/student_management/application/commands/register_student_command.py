from injector import inject

from src.modules.common.application import UnitOfWork, UseCase
from src.modules.student_management.application.gateways import (
    AttendanceModuleGateway,
    EduInfoModuleGateway,
)
from src.modules.student_management.application.repositories import CacheStudentDataRepository, StudentRepository
from src.modules.student_management.domain import Role, Student


class RegisterStudentCommand(UseCase):
    _cache_student_repository: CacheStudentDataRepository
    _student_repository: StudentRepository
    _edu_info_module_gateway: EduInfoModuleGateway
    _attendance_module_gateway: AttendanceModuleGateway
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        student_repostory: StudentRepository,
        cache_student_data_repository: CacheStudentDataRepository,
        edu_info_module_gateway: EduInfoModuleGateway,
        attendance_module_gateway: AttendanceModuleGateway,
        uow: UnitOfWork,
    ) -> None:
        self._cache_student_repository = cache_student_data_repository
        self._student_repository = student_repostory
        self._edu_info_module_gateway = edu_info_module_gateway
        self._attendance_module_gateway = attendance_module_gateway
        self._uow = uow

    async def execute(self, telegram_id: int) -> Student:
        async with self._uow:
            create_student_data = await self._cache_student_repository.pop(telegram_id)

            if create_student_data is None:
                raise RuntimeError("Not found user data in cache.")

            student_university = await self._edu_info_module_gateway.get_university_info_by_alias(
                create_student_data.university_alias,
            )
            student_group = await self._edu_info_module_gateway.find_group_by_name(create_student_data.group_name)

            if student_group is None and create_student_data.role < Role.HEADMAN:
                raise RuntimeError(
                    "For students with role 'student' and 'vice headman' group must already have been created before.",
                )

            if student_group is None:
                student_group = await self._edu_info_module_gateway.create_group(
                    create_student_data.group_name,
                    student_university.id,
                )

            student = await self._student_repository.create(create_student_data, student_group.id)
            await self._attendance_module_gateway.create_attendance(
                student.id,
                create_student_data.university_alias,
                student_group.id,
                student_group.name,
            )

        return student
