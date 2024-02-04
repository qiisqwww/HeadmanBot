from typing import final

from asyncpg import Record

from src.modules.common.domain import UniversityAlias
from src.modules.edu_info.domain import University

__all__ = [
    "UniversityMapper",
]


@final
class UniversityMapper:
    def to_domain(self, data: Record)-> University:
        return University(
            id=data["id"],
            name=data["name"],
            alias=UniversityAlias(data["alias"]),
        )
