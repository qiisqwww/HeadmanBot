from typing import final

from asyncpg import Record

from src.modules.edu_info.domain import GroupInfo

__all__ = [
    "GroupInfoMapper",
]


@final
class GroupInfoMapper:
    def to_domain(self, data: Record) -> GroupInfo:
        return GroupInfo(
            id=data["id"],
            name=data["name"],
            university_alias=data["alias"],
        )
