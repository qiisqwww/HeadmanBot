from dependency_injector.containers import DeclarativeContainer

from src.modules.common.infrastructure.database import (
    get_postgres_connection,
    get_redis_connection,
)
from src.modules.edu_info.infrastructure.contract import EduInfoModuleContractImpl
from src.modules.edu_info.infrastructure.persistence import (
    GroupRepositoryImpl,
    UniversityRepositoryImpl,
)
from src.modules.student_management.infrastructure.container import (
    assemble_student_management_container,
)

__all__ = [
    "assemble_project_containers",
]


async def assemble_project_containers() -> list[DeclarativeContainer]:
    postgres_connection = await anext(get_postgres_connection())
    redis_connection = await anext(get_redis_connection())

    university_repository = UniversityRepositoryImpl(postgres_connection)
    group_repository = GroupRepositoryImpl(postgres_connection)

    return [
        assemble_student_management_container(
            postgres_connection, redis_connection, EduInfoModuleContractImpl(university_repository, group_repository)
        )
    ]
