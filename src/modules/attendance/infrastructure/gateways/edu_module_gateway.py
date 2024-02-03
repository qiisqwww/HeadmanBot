from typing import final

from injector import inject

from src.modules.attendance.application.gateways import EduInfoModuleGateway
from src.modules.attendance.domain import GroupInfo
from src.modules.edu_info.contract import EduInfoModuleContract

__all__ = [
    "EduInfoModuleGatewayImpl",
]


@final
class EduInfoModuleGatewayImpl(EduInfoModuleGateway):
    _contract: EduInfoModuleContract

    @inject
    def __init__(self, contract: EduInfoModuleContract) -> None:
        self._contract = contract

    async def fetch_all_groups(self) -> list[GroupInfo]:
        return [GroupInfo(**group_info) for group_info in await self._contract.fetch_all_groups_info()]
