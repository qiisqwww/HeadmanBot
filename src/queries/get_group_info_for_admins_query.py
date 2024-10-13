from typing import final

from injector import inject

from src.common import UseCase
from src.modules.edu_info.application.gateways import StudentManagementGateway
from src.modules.edu_info.application.repositories import GroupRepository
from src.modules.edu_info.domain.models import GroupAdminInfo
from src.modules.edu_info.infrastructure.mappers import GroupAdminInfoMapper

__all__ = [
    "GetGroupInfoForAdminsQuery",
]


@final
class GetGroupInfoForAdminsQuery(UseCase):
    _repository: GroupRepository
    _gateway: StudentManagementGateway
    _mapper: GroupAdminInfoMapper = GroupAdminInfoMapper()

    @inject
    def __init__(self, repository: GroupRepository, _gateway: StudentManagementGateway) -> None:
        self._repository = repository
        self._gateway = _gateway

    async def execute(self) -> list[GroupAdminInfo]:
        groups = await self._repository.all()

        return [self._mapper.to_domain(group, await self._gateway.get_headman_by_group_id(group.id)) for group in
                groups]
