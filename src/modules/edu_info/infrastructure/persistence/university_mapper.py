from collections.abc import Mapping

from src.modules.common.domain import UniversityAlias
from src.modules.edu_info.domain import University

__all__ = [
    "UniversityMapper",
]


class UniversityMapper:
    def to_domain(self, mapped_data: Mapping) -> University:
        return University(
            id=mapped_data["id"],
            name=mapped_data["name"],
            alias=UniversityAlias(mapped_data["alias"]),
        )
