from collections.abc import Mapping
from typing import final

from src.modules.student_management.domain import Role, Student

__all__ = [
    "StudentMapper",
]


@final
class StudentMapper:
    def to_domain(self, record: Mapping) -> Student:
        return Student(
            id=record["id"],
            telegram_id=record["telegram_id"],
            name=record["name"],
            surname=record["surname"],
            group_id=record["group_id"],
            role=Role(record["role"]),
            birthdate=record["birthdate"],
            is_checked_in_today=record["is_checked_in_today"],
        )
