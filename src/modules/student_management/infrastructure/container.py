from asyncpg.pool import PoolConnectionProxy
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from redis.asyncio import Redis

from src.modules.common.infrastructure.apis.schedule_api import ScheduleApiImpl
from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.student_management.application.commands import (
    CacheCreateStudentDataCommand,
    ClearCreateStudentDataCacheCommand,
)
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupHeadmanQuery,
    FindStudentQuery,
    GetAllUniversitiesQuery,
)

from .gateways import EduInfoModuleGatewayImpl
from .persistance import CacheStudentDataRepositoryImpl, StudentRepositoryImpl

__all__ = [
    "assemble_student_management_container",
]


class StudentManagementContainer(DeclarativeContainer):
    db_con = Dependency(instance_of=PoolConnectionProxy)
    redis_con = Dependency(instance_of=Redis)
    edu_info_module_contract = Dependency(instance_of=EduInfoModuleContract)

    student_repository = Singleton(StudentRepositoryImpl, db_con)
    cache_student_data_repository = Singleton(CacheStudentDataRepositoryImpl, redis_con)
    edu_info_module_gateway = Singleton(EduInfoModuleGatewayImpl, edu_info_module_contract)

    find_student_query = Singleton(FindStudentQuery, student_repository)
    find_group_headman_query = Singleton(FindGroupHeadmanQuery, student_repository)
    # register_student_command = Singleton(
    #     RegisterStudentCommand,
    #     student_repository=student_repository,
    #     group_repository=group_repository,
    #     university_repository=university_repository,
    #     cache_student_data_repository=cache_student_data_repository,
    # )

    cache_create_student_data_command = Singleton(CacheCreateStudentDataCommand, cache_student_data_repository)
    clear_create_student_data_command = Singleton(ClearCreateStudentDataCacheCommand, cache_student_data_repository)

    # get_university_by_alias_query = Singleton(GetUniversityByAliasQuery, university_repository)
    get_all_universities_query = Singleton(GetAllUniversitiesQuery, edu_info_module_gateway)

    check_group_exists_in_uni_query = Singleton(CheckGroupExistsInUniQuery, ScheduleApiImpl)

    # is_group_registered_query = Singleton(IsGroupRegisteredQuery, group_repository)


def assemble_student_management_container(
    database_connection: PoolConnectionProxy, redis_connection: Redis, edu_info_module_contract: EduInfoModuleContract
) -> DeclarativeContainer:
    return StudentManagementContainer(
        db_con=database_connection,
        redis_con=redis_connection,
        edu_info_module_contract=edu_info_module_contract,
    )
