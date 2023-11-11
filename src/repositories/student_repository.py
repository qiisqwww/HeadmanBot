from typing import Any, Mapping

from src.dto import Student

from .asyncpg_repository import AsyncpgRepository

__all__ = [
    "StudentRepository",
]


class StudentRepository(AsyncpgRepository[Student]):
    async def get(self, id: int) -> Student | None:
        query = "SELECT * FROM students WHERE id = $1"
        record = await self._con.fetchrow(query, id)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def all(self) -> list[Student]:
        query = "SELECT * from students"
        records = await self._con.fetch(query)

        return [Student.from_mapping(record) for record in records]

    async def create(self, data: Mapping) -> Student:
        query = (
            "INSERT INTO students "
            "(telegram_id, group_id, university_id, name, surname, telegram_name, is_headman)"
            " VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id"
        )
        await self._con.execute(
            query,
            data["telegram_id"],
            data["group_id"],
            data["university_id"],
            data["name"],
            data["surname"],
            data["telegram_name"],
            data["is_headman"],
        )

        return Student(
            telegram_id=data["telegram_id"],
            group_id=data["group_id"],
            university_id=data["university_id"],
            name=data["name"],
            surname=data["surname"],
            telegram_name=data["telegram_name"],
            is_headman=data["is_headman"],
        )

    async def update(self, dto: Student) -> Student:
        query = (
            "UPDATE students SET "
            "telegram_id=$1, group_id=$2, university_id=$3, name=$4, surname=$5, telegram_name=$6, is_headman=$7 "
            "WHERE telegram_id=$8"
        )

        await self._con.execute(
            query,
            dto.telegram_id,
            dto.group_id,
            dto.university_id,
            dto.name,
            dto.surname,
            dto.telegram_name,
            dto.is_headman,
            dto.telegram_id,
        )

        return dto

    async def patch(self, dto: Student, column: str, new_value: Any) -> Student:
        query = "UPDATE universities SET $1=$2 WHERE telegram_id=$3"
        await self._con.execute(query, column, new_value, dto.telegram_id)
        setattr(dto, column, new_value)
        return dto

    async def delete(self, dto: Student) -> None:
        query = "DELETE FROM students WHERE telegram_id = $1"
        await self._con.execute(query, dto.telegram_id)

    async def filter_by_group(self, group_id: int) -> list[Student] | None:
        query = "SELECT * FROM students WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        if records is None:
            return None

        return [Student.from_mapping(record) for record in records]
