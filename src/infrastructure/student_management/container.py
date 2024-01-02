from asyncpg.pool import PoolConnectionProxy
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from redis.asyncio import Redis

from src.application.student_management.commands import CacheCreateStudentDataCommand
from src.application.student_management.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupHeadmanQuery,
    FindStudentQuery,
    GetAllUniversitiesQuery,
    GetUniversityByAliasQuery,
    IsGroupRegisteredQuery,
)
from src.infrastructure.common.apis.schedule_api import ScheduleApiImpl
from src.infrastructure.edu_info.persistence import (
    GroupRepositoryImpl,
    UniversityRepositoryImpl,
)

from .persistance import CacheStudentDataRepositoryImpl, StudentRepositoryImpl

__all__ = [
    "StudentManagementContainer",
]


class StudentManagementContainer(DeclarativeContainer):
    db_con = Dependency(instance_of=PoolConnectionProxy)
    redis_con = Dependency(instance_of=Redis)

    student_repository = Singleton(StudentRepositoryImpl, db_con)
    cache_student_data_repository = Singleton(CacheStudentDataRepositoryImpl, redis_con)
    university_repository = Singleton(UniversityRepositoryImpl, db_con)
    group_repository = Singleton(GroupRepositoryImpl, db_con)

    find_student_query = Singleton(FindStudentQuery, student_repository)
    find_group_headman_query = Singleton(FindGroupHeadmanQuery, student_repository)

    cache_student_data_repository = Singleton(CacheCreateStudentDataCommand, cache_student_data_repository)

    get_university_by_alias_query = Singleton(GetUniversityByAliasQuery, university_repository)
    get_all_universities_query = Singleton(GetAllUniversitiesQuery, university_repository)

    check_group_exists_in_uni_query = Singleton(CheckGroupExistsInUniQuery, ScheduleApiImpl)

    is_group_registered_query = Singleton(IsGroupRegisteredQuery, group_repository)
