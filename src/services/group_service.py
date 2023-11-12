from src.dto import Group, Student

from .exceptions import CorruptedDatabaseError
from .service import Service

__all__ = [
    "GroupService",
]


class GroupService(Service):
    async def try_create_or_return(self, name: str) -> Group:
        """Trying to create new group or return if it exists."""
        group = await self.get_by_name(name)

        if group is not None:
            return group

        return await self._create(name)

    async def get_by_name(self, name: str) -> Group | None:
        query = "SELECT id FROM groups WHERE name LIKE $1"
        pk = await self._con.fetchval(query, name)

        if pk is None:
            return None

        return Group(
            id=pk,
            name=name,
        )

    async def get_by_student(self, student: Student) -> Group:
        query = "SELECT name FROM groups WHERE id = $1"
        name = await self._con.fetchval(query, student.group_id)

        if name is None:
            raise CorruptedDatabaseError(
                f"Group for student with id={student.telegram_name} {student.surname} {student.name} does not exists."
            )

        return Group(
            id=student.group_id,
            name=name,
        )

    async def all(self) -> list[Group]:
        query = "SELECT * FROM groups"
        records = await self._con.fetch(query)

        return [Group.from_mapping(record) for record in records]

    async def _create(self, name: str) -> Group:
        query = "INSERT INTO groups (name) VALUES ($1) RETURNING id"
        pk = await self._con.fetchval(query, name)

        return Group(
            id=pk,
            name=name,
        )
