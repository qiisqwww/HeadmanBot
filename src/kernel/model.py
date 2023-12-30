from abc import ABC, abstractmethod
from enum import Enum
from types import NoneType, UnionType
from typing import Mapping, NoReturn, Self

__all__ = [
    "Model",
]


class Model(ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        ...

    @classmethod
    def from_mapping(cls: type[Self], data: Mapping) -> Self:
        """This constructor convert enum types, do type checking and
        set None for args which can be None but not passed into data mapping."""
        validated_data = {}

        model_annotations = cls.__annotations__.items()

        for attribute_name, attribute_type in model_annotations:
            if isinstance(attribute_type, UnionType):
                cls._validate_union_type(attribute_type)  # Check is union type is optional.
                attribute_types = attribute_type.__args__
                attribute_type = (
                    attribute_types[1] if attribute_types[0] == NoneType else attribute_types[0]
                )  # Get real type from Optional.

            else:
                if (
                    data.get(attribute_name) is None
                ):  # If value is None or argument not passed and type is not optional it is error.
                    raise ValueError(f"You must pass '{attribute_name}' argument to model.")

            if data.get(attribute_name, None) is None:
                attribute_value = None
            elif isinstance(attribute_type, type) and issubclass(
                attribute_type, Enum
            ):  # In project we don't store enum in database and due this
                # we must convert types from str or something else to enum.
                attribute_value = attribute_type(data[attribute_name])
            else:
                attribute_value = data[attribute_name]

            validated_data[attribute_name] = attribute_value

        cls._check_types(validated_data)

        return cls(**validated_data)

    @staticmethod
    def _validate_union_type(union_type: UnionType) -> None | NoReturn:
        """Check is union type is Optional or not."""
        types = union_type.__args__

        if len(types) > 2:  # Check for complex union like int | str | None and more types.
            raise ValueError("Don't support complex UnionType only simple types or Optional type.")
        if NoneType not in types:  # Check for complex union with two types, but not Optional
            raise ValueError("Don't support complex UnionType only simple types or Optional type.")

        return None

    @classmethod
    def _check_types(cls, validated_data: Mapping) -> None | NoReturn:
        model_annotations = cls.__annotations__.items()

        for attribute_name, attribute_type in model_annotations:
            if isinstance(attribute_type, type) and not isinstance(validated_data[attribute_name], attribute_type):
                raise TypeError(
                    f"attribute '{attribute_name}' must have type '{attribute_type}' "
                    f"but '{type(validated_data[attribute_name])}' was passed."
                )

        return None
