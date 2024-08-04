
from injector import inject

from src.modules.common.application import UnitOfWork, UseCase
from src.modules.student_management.application.gateways import (
    AttendanceModuleGateway,
    EduInfoModuleGateway,
)
from src.modules.student_management.application.repositories import (
    CacheStudentEnterGroupDataRepository,
    StudentRepository,
)
from src.modules.student_management.domain import Role, Student

__all__ = [
    "StudentAlreadyEnteredGroupError",
    "NotFoundStudentEnterGroupCachedDataError",
    "StudentEnterGroupCommand",
]


class StudentAlreadyEnteredGroupError(RuntimeError):
    """Raise if student already entered the group. For example, headman was already accepted by first
    admin but second also have clicked accept button.
    """


class NotFoundStudentEnterGroupCachedDataError(RuntimeError):
    """Cached student data for its creation was not found.
    May be because of expire date.
    """


class StudentEnterGroupCommand(UseCase):
    _cache_student_enter_group_data_repository: CacheStudentEnterGroupDataRepository
    _student_repository: StudentRepository
    _edu_info_module_gateway: EduInfoModuleGateway
    _attendance_module_gateway: AttendanceModuleGateway
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        student_repository: StudentRepository,
        cache_student_enter_group_data_repository: CacheStudentEnterGroupDataRepository,
        edu_info_module_gateway: EduInfoModuleGateway,
        attendance_module_gateway: AttendanceModuleGateway,
        uow: UnitOfWork,
    ) -> None:
        self._cache_student_enter_group_data_repository = cache_student_enter_group_data_repository
        self._student_repository = student_repository
        self._edu_info_module_gateway = edu_info_module_gateway
        self._attendance_module_gateway = attendance_module_gateway
        self._uow = uow

    async def execute(self, telegram_id: int) -> Student:
        async with self._uow:
            create_student_data = await self._cache_student_enter_group_data_repository.fetch(
                telegram_id,
            )

            if create_student_data is None:
                student = await self._student_repository.find_by_telegram_id(
                    telegram_id,
                )

                if student.group_id is not None:
                    raise StudentAlreadyEnteredGroupError
                raise NotFoundStudentEnterGroupCachedDataError

            student_university = (
                await self._edu_info_module_gateway.get_university_info_by_alias(
                    create_student_data.university_alias,
                )
            )
            student_group = await self._edu_info_module_gateway.find_group_by_name(
                create_student_data.group_name,
            )

            if student_group is None and create_student_data.role < Role.HEADMAN:
                msg = "For students with role 'student' and 'vice headman' group must already have been created before."
                raise RuntimeError(
                    msg,
                )

            if student_group is None:
                student_group = await self._edu_info_module_gateway.create_group(
                    create_student_data.group_name,
                    student_university.id,
                )

            await self._student_repository.enter_group_by_telegram_id(
                create_student_data,
                student_group.id,
            )

            student = await self._student_repository.find_by_telegram_id(create_student_data.telegram_id)

            await self._attendance_module_gateway.create_attendance(
                student.id,
                create_student_data.university_alias,
                student_group.id,
                student_group.name,
            )

            await self._cache_student_enter_group_data_repository.delete(telegram_id)

        return student
