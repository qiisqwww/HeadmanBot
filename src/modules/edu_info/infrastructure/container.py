from injector import Binder, singleton

from src.modules.edu_info.application.repositories import (
    EduInfoRepository,
    GroupRepository,
    UniversityRepository,
)
from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.edu_info.infrastructure.contract import EduInfoModuleContractImpl
from src.modules.edu_info.infrastructure.persistence import (
    EduInfoRepositoryImpl,
    GroupRepositoryImpl,
    UniversityRepositoryImpl,
)

__all__ = [
    "assemble_edu_info_module",
]


def singleton_bind(binder: Binder, interface, to) -> None:
    binder.bind(interface, to, singleton)


def assemble_edu_info_module(binder: Binder) -> None:
    singleton_bind(binder, GroupRepository, GroupRepositoryImpl)
    singleton_bind(binder, UniversityRepository, UniversityRepositoryImpl)
    singleton_bind(binder, EduInfoRepository, EduInfoRepositoryImpl)
    singleton_bind(binder, EduInfoModuleContract, EduInfoModuleContractImpl)
