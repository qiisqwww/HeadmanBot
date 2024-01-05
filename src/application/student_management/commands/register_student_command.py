from src.application.edu_info.repositories import GroupRepository, UniversityRepository
from src.domain.student_management import Role, Student

from ..repositories import CacheStudentDataRepository, StudentRepository


class RegisterStudentCommand:
    _cache_student_repository: CacheStudentDataRepository
    _student_repository: StudentRepository
    _university_repostory: UniversityRepository
    _group_repository: GroupRepository

    def __init__(
        self,
        student_repostory: StudentRepository,
        cache_student_data_repository: CacheStudentDataRepository,
        university_repository: UniversityRepository,
        group_repository: GroupRepository,
    ) -> None:
        self._cache_student_repository = cache_student_data_repository
        self._student_repository = student_repostory
        self._university_repostory = university_repository
        self._group_repository = group_repository

    async def execute(self, telegram_id: int) -> Student:
        create_student_data = await self._cache_student_repository.pop(telegram_id)

        if create_student_data is None:
            raise RuntimeError("Not found user data in cache.")

        student_university = await self._university_repostory.get_by_alias(create_student_data.university_alias)
        student_group = await self._group_repository.find_by_name(create_student_data.group_name)

        if student_group is None and create_student_data.role < Role.HEADMAN:
            raise RuntimeError(
                "For students with role 'student' and 'vice headman' group must already have been created before."
            )

        if student_group is None:
            student_group = await self._group_repository.create(create_student_data.group_name, student_university.id)

        student = await self._student_repository.create(create_student_data, student_group.id)

        return student
