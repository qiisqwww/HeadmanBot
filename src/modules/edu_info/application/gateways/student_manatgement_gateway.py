from abc import ABC, abstractmethod

__all__ = [
    "StudentManagementGateway",
]


class StudentManagementGateway(ABC):
    @abstractmethod
    async def get_headman_by_group_id(self, group_id: int) -> dict:
        ...
