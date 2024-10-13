from injector import inject

from src.common import UseCase
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.application.repositories import StudentRepository

__all__ = [
    "ChangeAdminGroupCommand",
    "GroupWasNotRegisteredException",
    "GroupBelongsToAnotherUviException"
]


class GroupWasNotRegisteredException(Exception):
    """
    Raised when admin is trying to get into the group that was not registered.
    """


class GroupBelongsToAnotherUviException(Exception):
    """
    Raised when required group exists but in another university.
    """


class ChangeAdminGroupCommand(UseCase):
    _repository: StudentRepository
    _gateway: EduInfoModuleGateway

    @inject
    def __init__(self, repository: StudentRepository, gateway: EduInfoModuleGateway) -> None:
        self._repository = repository
        self._gateway = gateway

    async def execute(self, telegram_id: int, group_name: str, university_id: int) -> None:
        group = await self._gateway.find_group_by_name(group_name)

        if group is None:
            raise GroupWasNotRegisteredException()
        if group.university_id != university_id:
            raise GroupBelongsToAnotherUviException()

        await self._repository.change_admin_group_by_telegram_id(telegram_id, group.id)
