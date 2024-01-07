from typing import Mapping

from src.modules.student_management.domain import Group, Role, Student

__all__ = [
    "StudentMapper",
]


class StudentMapper:
    def to_domain(self, record: Mapping) -> Student:
        group = Group(
            id=record["group_id"],
            name=record["group_name"],
            university_id=record["university_id"],
        )

        return Student(
            id=record["id"],
            telegram_id=record["telegram_id"],
            name=record["name"],
            surname=record["surname"],
            group=group,
            role=Role(record["role"]),
            birthdate=record["birthdate"],
            is_checked_in_today=record["is_checked_in_today"],
        )
