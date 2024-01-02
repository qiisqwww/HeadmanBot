from asyncpg.pool import PoolConnectionProxy
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from src.application.student_management.queries import (
    CheckGroupExistsInUniQuery,
    FindStudentQuery,
    GetAllUniversitiesQuery,
    GetUniversityByAliasQuery,
)
from src.infrastructure.common.apis.schedule_api import ScheduleApiImpl
from src.infrastructure.edu_info.persistence import UniversityRepositoryImpl

from .persistance import StudentRepositoryImpl

__all__ = [
    "StudentManagementContainer",
]


class StudentManagementContainer(DeclarativeContainer):
    db_con = Dependency(instance_of=PoolConnectionProxy)

    student_repository = Singleton(StudentRepositoryImpl, db_con)
    university_repository = Singleton(UniversityRepositoryImpl, db_con)

    find_student_query = Singleton(
        FindStudentQuery,
        student_repository,
    )

    get_university_by_alias_query = Singleton(
        GetUniversityByAliasQuery,
        university_repository,
    )

    get_all_universities_query = Singleton(
        GetAllUniversitiesQuery,
        university_repository,
    )

    check_group_exists_in_uni_query = Singleton(
        CheckGroupExistsInUniQuery,
        ScheduleApiImpl,
    )
