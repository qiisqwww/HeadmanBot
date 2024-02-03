from typing import Mapping, final

from src.modules.edu_info.domain import GroupInfo

__all__ = [
    "GroupInfoMapper",
]


@final 
class GroupInfoMapper:
    def to_domain(self, data: Mapping) -> GroupInfo:
        return GroupInfo(
            id=data['id'],
            name=data['name'],
            university_alias=data['alias'],
        )
