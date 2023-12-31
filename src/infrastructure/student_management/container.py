from asyncpg.pool import PoolConnectionProxy
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, Singleton

from src.application.student_management.queries import FindStudentQuery

from .persistance import StudentRepositoryImpl

__all__ = [
    "StudentManagementContainer",
]


class StudentManagementContainer(DeclarativeContainer):
    db_con = Dependency(instance_of=PoolConnectionProxy)
    student_repository = Singleton(StudentRepositoryImpl, con=db_con)

    find_student_query = Factory(
        FindStudentQuery,
        repository=student_repository,
    )
