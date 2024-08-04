from injector import Binder, singleton

from src.modules.edu_info.application.gateways import StudentManagementGateway
from src.modules.edu_info.application.repositories import (
    EduInfoRepository,
    GroupInfoRepository,
    GroupRepository,
    UniversityRepository,
)
from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.edu_info.infrastructure.gateways import StudentManagementGatewayImpl

from .contract import EduInfoModuleContractImpl
from .repositories import (
    EduInfoRepositoryImpl,
    GroupInfoRepositoryImpl,
    GroupRepositoryImpl,
    UniversityRepositoryImpl,
)

__all__ = [
    "assemble_edu_info_module",
]


def assemble_edu_info_module(binder: Binder) -> None:
    binder.bind(GroupRepository, GroupRepositoryImpl, singleton)
    binder.bind(UniversityRepository, UniversityRepositoryImpl, singleton)
    binder.bind(EduInfoRepository, EduInfoRepositoryImpl, singleton)
    binder.bind(GroupInfoRepository, GroupInfoRepositoryImpl, singleton)

    binder.bind(StudentManagementGateway, StudentManagementGatewayImpl, singleton)
    binder.bind(EduInfoModuleContract, EduInfoModuleContractImpl, singleton)

