from abc import ABC, abstractmethod
from typing import Mapping, Self


class DTO(ABC):
    @classmethod
    @abstractmethod
    def from_mapping(cls, data: Mapping) -> Self:
        ...
