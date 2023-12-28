from dataclasses import dataclass
from datetime import date
from enum import IntEnum, StrEnum
from typing import Mapping

import pytest

from src.dto.models.model import Model


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class SomeUndefinedEnum(IntEnum):
    PROPERTY1 = 1
    PROPERTY2 = 2


@dataclass(slots=True, frozen=True)
class StudentLoginData(Model):
    telegram_id: int
    name: str
    birthdate: date | None
    some_enum: SomeUndefinedEnum | None
    role: Role


@dataclass
class InvalidModel1(Model):
    data: str | int


@dataclass
class InvalidModel2(Model):
    data: str | int | None


@dataclass
class InvalidModel3(Model):
    data: str | int | date


@pytest.mark.parametrize(
    "mapping,result_model",
    [
        (
            {
                "telegram_id": 1,
                "name": "name21",
                "surname": "nice surname",
                "birthdate": None,
                "role": "ADMIN",
            },
            StudentLoginData(telegram_id=1, name="name21", birthdate=None, role=Role.ADMIN, some_enum=None),
        ),
        (
            {
                "telegram_id": 32,
                "name": "name432",
                "role": "USER",
                "some_enum": 1,
            },
            StudentLoginData(
                telegram_id=32, name="name432", birthdate=None, role=Role.USER, some_enum=SomeUndefinedEnum.PROPERTY1
            ),
        ),
    ],
)
def test_from_mapping(mapping: Mapping, result_model: StudentLoginData) -> None:
    assert StudentLoginData.from_mapping(mapping) == result_model


@pytest.mark.parametrize(
    "mapping,result_model_type",
    [
        ({"data": "data"}, InvalidModel1),
        ({"data": "data"}, InvalidModel2),
        ({"data": "data"}, InvalidModel3),
    ],
)
def test_unssuported_model_annotations(mapping: Mapping, result_model_type: type[Model]):
    with pytest.raises(ValueError):
        result_model_type.from_mapping(mapping)
