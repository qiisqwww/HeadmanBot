from types import NoneType, UnionType
from typing import Mapping, Self

__all__ = [
    "DTO",
]


class DTO:
    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        valid_attrs = {}

        for attr_name, attr_type in cls.__annotations__.items():
            if isinstance(attr_type, UnionType):
                annotations = attr_type.__args__
                if len(annotations) > 2:  # Check for complex union like int | str | None and more types.
                    raise ValueError("Don't support complex UnionType only simple types or Optional type.")
                if NoneType not in annotations:  # Check for complex union with two types, but not Optional
                    raise ValueError("Don't support complex UnionType only simple types or Optional type.")

                attr_type = annotations[1] if annotations[0] == NoneType else annotations[0]

                if data[attr_name] is None:
                    attr_value = None
                else:
                    attr_value = attr_type(data[attr_name])

            else:
                attr_value = attr_type(data[attr_name])

            valid_attrs[attr_name] = attr_value

        return cls(**valid_attrs)
