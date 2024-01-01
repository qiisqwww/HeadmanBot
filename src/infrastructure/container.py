from dependency_injector import containers
from dependency_injector.containers import DeclarativeContainer

from .student_management.container import StudentManagementContainer

__all__ = [
    "HeadmanDIContainer",
]


@containers.copy(StudentManagementContainer)
class HeadmanDIContainer(DeclarativeContainer):
    ...
