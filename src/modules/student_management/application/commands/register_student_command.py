from injector import inject

from src.modules.common.application import Dependency
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import Role, Student

from ..repositories import CacheStudentDataRepository, StudentRepository


class RegisterStudentCommand(Dependency):
    _cache_student_repository: CacheStudentDataRepository
    _student_repository: StudentRepository
    _edu_info_module_gateway: EduInfoModuleGateway

    @inject
    def __init__(
        self,
        student_repostory: StudentRepository,
        cache_student_data_repository: CacheStudentDataRepository,
        edu_info_module_gateway: EduInfoModuleGateway,
    ) -> None:
        self._cache_student_repository = cache_student_data_repository
        self._student_repository = student_repostory
        self._edu_info_module_gateway = edu_info_module_gateway

    async def execute(self, telegram_id: int) -> Student:
        create_student_data = await self._cache_student_repository.pop(telegram_id)

        if create_student_data is None:
            raise RuntimeError("Not found user data in cache.")

        student_university = await self._edu_info_module_gateway.get_university_info_by_alias(
            create_student_data.university_alias
        )
        student_group = await self._edu_info_module_gateway.find_group_by_name(create_student_data.group_name)

        if student_group is None and create_student_data.role < Role.HEADMAN:
            raise RuntimeError(
                "For students with role 'student' and 'vice headman' group must already have been created before."
            )

        if student_group is None:
            student_group = await self._edu_info_module_gateway.create_group(
                create_student_data.group_name, student_university.id
            )

        student = await self._student_repository.create(create_student_data, student_group)

        return student
