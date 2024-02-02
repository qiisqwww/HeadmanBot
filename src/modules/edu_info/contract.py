from abc import ABC, abstractmethod
from typing import Any

from src.modules.common.domain import UniversityAlias

__all__ = [
    "EduInfoModuleContract",
]


class EduInfoModuleContract(ABC):
    @abstractmethod
    async def get_group_info_by_group_id(self, group_id: int) -> dict[str, Any] | None:
        """Return data like a dict

        return_value['id']: int -> group id
        return_value['name']: str -> group name
        return_value['university_id']: str -> university id

        """

    @abstractmethod
    async def get_group_info_by_group_name(self, group_name: str) -> dict[str, Any] | None:
        """Return data like a dict

        return_value['id']: int -> group id
        return_value['name']: str -> group name
        return_value['university_id']: str -> university id

        """

    @abstractmethod
    async def get_group_info_by_group_name_and_alias(
        self, group_name: str, alias: UniversityAlias
    ) -> dict[str, Any] | None:
        """Return data like a dict

        return_value['id']: int -> group id
        return_value['name']: str -> group name
        return_value['university_id']: str -> university id

        """

    @abstractmethod
    async def create_group(self, group_name: str, university_id: int) -> dict[str, Any]:
        """Return data like a dict

        return_value['id']: int -> group id
        return_value['name']: str -> group name
        return_value['university_id']: str -> university id

        """

    @abstractmethod
    async def get_all_universities_info(self) -> list[dict[str, Any]]:
        """Return data like a list of dicts
        university_info = return_value[0]

        university_info['id']: int -> university id
        university_info['name']: str -> university name
        university_info['alias']: UniversityAlias -> university alias
        """

    @abstractmethod
    async def get_university_info_by_alias(self, alias: UniversityAlias) -> dict[str, Any]:
        """Return data like a list of dicts

        return_value['id']: int -> university id
        return_value['name']: str -> university name
        return_value['alias']: UniversityAlias -> university alias
        """

    @abstractmethod
    async def get_group_name_and_uni_name(self, group_id: int) -> tuple[str, str] | None:
        """Return data like a tuple
        return_value[0]: str -> group_name
        return_value[1]: str -> university_name"""

    @abstractmethod 
    async def fetch_all_groups_info(self) -> list[dict[str, Any]]:
        """Return data like a list of dicts
        group_info = return_value[0]

        group_info['id']: int -> group id
        group_info['name']: str -> group name
        group_info['university_alias']: UniversityAlias -> university alias
        """
