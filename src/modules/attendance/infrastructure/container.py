from injector import Binder, singleton

from src.modules.attendance.application.gateways import EduInfoModuleGateway, StudentManagementGateway
from src.modules.attendance.application.repositories import (
    AttendanceRepository,
    GroupAttendanceRepository,
    LessonRepository,
)
from src.modules.attendance.contract import AttendanceModuleContract

from .contract import AttendanceModuleContractImpl
from .gateways import EduInfoModuleGatewayImpl, StudentManagementGatewayImpl
from .repositories import (
    AttendanceRepositoryImpl,
    GroupAttendanceRepositoryImpl,
    LessonRepositoryImpl,
)

__all__ = [
    "assemble_attendance_module",
]


def assemble_attendance_module(binder: Binder) -> None:
    binder.bind(AttendanceRepository, AttendanceRepositoryImpl, singleton)
    binder.bind(LessonRepository, LessonRepositoryImpl, singleton)
    binder.bind(GroupAttendanceRepository, GroupAttendanceRepositoryImpl, singleton)

    binder.bind(AttendanceModuleContract, AttendanceModuleContractImpl, singleton)

    binder.bind(StudentManagementGateway, StudentManagementGatewayImpl, singleton)
    binder.bind(EduInfoModuleGateway, EduInfoModuleGatewayImpl, singleton)
