from typing import Mapping

from src.modules.edu_info.domain import Group

__all__ = [
    "GroupMapper",
]


class GroupMapper:
    def to_domain(self, mapped_data: Mapping) -> Group:
        return Group(
            id=mapped_data["id"],
            name=mapped_data["name"],
            university_id=mapped_data["university_id"],
        )
