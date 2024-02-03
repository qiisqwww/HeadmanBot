from typing import final

from asyncpg import Record

from src.modules.edu_info.domain import Group

__all__ = [
    "GroupMapper",
]


@final
class GroupMapper:
    def to_domain(self, data: Record) -> Group:
        return Group(
            id=data["id"],
            name=data["name"],
            university_id=data["university_id"],
        )
