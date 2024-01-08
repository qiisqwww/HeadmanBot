from abc import abstractmethod
from typing import Any

from src.modules.common.application import Dependency
from src.modules.common.domain.university_alias import UniversityAlias

__all__ = [
    "EduInfoModuleContract",
]


class EduInfoModuleContract(Dependency):
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
