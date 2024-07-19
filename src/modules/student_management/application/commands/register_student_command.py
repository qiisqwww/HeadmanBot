from typing import NoReturn

from injector import inject

from src.modules.common.application import UnitOfWork, UseCase
from src.modules.student_management.application.gateways import (
    AttendanceModuleGateway,
    EduInfoModuleGateway,
)
from src.modules.student_management.application.repositories import (
    CacheCreateStudentDataRepository,
    StudentRepository,
)
from src.modules.student_management.domain import Role, Student

__all__ = [
    "StudentAlreadyRegisteredError",
    "NotFoundStudentRegistrationCachedDataError",
    "RegisterStudentCommand",
]


class StudentAlreadyRegisteredError(RuntimeError):
    """Raise if student already exists. For example, headman was already accepted by first
    admin but second also have clicked accept button.
    """


class NotFoundStudentRegistrationCachedDataError(RuntimeError):
    """Cached student data for its creation was not found.
    May be because of expire date.
    """


class RegisterStudentCommand(UseCase):
    _cache_student_repository: CacheCreateStudentDataRepository
    _student_repository: StudentRepository
    _edu_info_module_gateway: EduInfoModuleGateway
    _attendance_module_gateway: AttendanceModuleGateway
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        student_repository: StudentRepository,
        cache_student_data_repository: CacheCreateStudentDataRepository,
        edu_info_module_gateway: EduInfoModuleGateway,
        attendance_module_gateway: AttendanceModuleGateway,
        uow: UnitOfWork,
    ) -> None:
        self._cache_student_repository = cache_student_data_repository
        self._student_repository = student_repository
        self._edu_info_module_gateway = edu_info_module_gateway
        self._attendance_module_gateway = attendance_module_gateway
        self._uow = uow

    async def execute(self, telegram_id: int) -> Student | NoReturn:
        async with self._uow:
            create_student_data = await self._cache_student_repository.fetch(
                telegram_id,
            )

            if create_student_data is None:
                student = await self._student_repository.find_by_telegram_id(
                    telegram_id,
                )

                if student is not None:
                    raise StudentAlreadyRegisteredError
                raise NotFoundStudentRegistrationCachedDataError

            student_university = (
                await self._edu_info_module_gateway.get_university_info_by_alias(
                    create_student_data.university_alias,
                )
            )
            student_group = await self._edu_info_module_gateway.find_group_by_name(
                create_student_data.group_name,
            )

            if student_group is None and create_student_data.role < Role.HEADMAN:
                raise RuntimeError(
                    "For students with role 'student' and 'vice headman' group must already have been created before.",
                )

            if student_group is None:
                student_group = await self._edu_info_module_gateway.create_group(
                    create_student_data.group_name,
                    student_university.id,
                )

            student = await self._student_repository.create(
                create_student_data,
                student_group.id,
            )
            await self._attendance_module_gateway.create_attendance(
                student.id,
                create_student_data.university_alias,
                student_group.id,
                student_group.name,
            )

            await self._cache_student_repository.delete(telegram_id)

        return student
