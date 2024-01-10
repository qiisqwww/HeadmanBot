from injector import Binder, singleton

from src.modules.student_management.application.gateways import (
    AttendanceModuleGateway,
    EduInfoModuleGateway,
)
from src.modules.student_management.application.repositories import (
    CacheStudentDataRepository,
    StudentRepository,
)

from .gateways import AttendanceModuleGatewayImpl, EduInfoModuleGatewayImpl
from .persistance import CacheStudentDataRepositoryImpl, StudentRepositoryImpl

__all__ = [
    "assemble_student_management_module",
]


def singleton_bind(binder: Binder, interface, to) -> None:
    binder.bind(interface, to, singleton)


def assemble_student_management_module(binder: Binder) -> None:
    singleton_bind(binder, StudentRepository, StudentRepositoryImpl)
    singleton_bind(binder, CacheStudentDataRepository, CacheStudentDataRepositoryImpl)
    singleton_bind(binder, EduInfoModuleGateway, EduInfoModuleGatewayImpl)
    singleton_bind(binder, AttendanceModuleGateway, AttendanceModuleGatewayImpl)
