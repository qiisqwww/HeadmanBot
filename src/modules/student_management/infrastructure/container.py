from injector import Binder, singleton

from src.modules.student_management.application.gateways import (
    AttendanceModuleGateway,
    EduInfoModuleGateway,
)
from src.modules.student_management.application.repositories import (
    CacheStudentDataRepository,
    StudentInfoRepository,
    StudentRepository,
)
from src.modules.student_management.contract import StudentManagementContract

from .contract import StudentManagementContractImpl
from .gateways import AttendanceModuleGatewayImpl, EduInfoModuleGatewayImpl
from .repositories import (
    CacheStudentDataRepositoryImpl,
    StudentInfoRepositoryImpl,
    StudentRepositoryImpl,
)

__all__ = [
    "assemble_student_management_module",
]

def assemble_student_management_module(binder: Binder) -> None:
    binder.bind(StudentRepository, StudentRepositoryImpl, singleton)
    binder.bind(CacheStudentDataRepository, CacheStudentDataRepositoryImpl, singleton)
    binder.bind(StudentInfoRepository, StudentInfoRepositoryImpl, singleton)

    binder.bind(EduInfoModuleGateway, EduInfoModuleGatewayImpl, singleton)
    binder.bind(AttendanceModuleGateway, AttendanceModuleGatewayImpl, singleton)

    binder.bind(StudentManagementContract, StudentManagementContractImpl, singleton)
