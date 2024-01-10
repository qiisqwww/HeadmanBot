from injector import Binder, singleton

from src.modules.attendance.application.commands import CreateAttendanceCommand
from src.modules.attendance.application.contract import AttendanceModuleContract
from src.modules.attendance.application.repositories import (
    AttendanceRepository,
    LessonRepository,
)
from src.modules.attendance.infrastructure.contract import AttendanceModuleContractImpl
from src.modules.attendance.infrastructure.persistence import (
    AttendanceRepositoryImpl,
    LessonRepositoryImpl,
)

__all__ = [
    "assemble_attendace_module",
]


def singleton_bind(binder: Binder, interface, to) -> None:
    binder.bind(interface, to, singleton)


def assemble_attendace_module(binder: Binder) -> None:
    singleton_bind(binder, AttendanceRepository, AttendanceRepositoryImpl)
    singleton_bind(binder, LessonRepository, LessonRepositoryImpl)
    singleton_bind(binder, CreateAttendanceCommand, CreateAttendanceCommand)
    singleton_bind(binder, AttendanceModuleContract, AttendanceModuleContractImpl)
