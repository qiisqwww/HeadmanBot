from typing import final

from src.modules.common.domain import UniversityAlias
from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl
from src.modules.edu_info.application.repositories import GroupRepository
from src.modules.edu_info.domain import Group
from src.modules.edu_info.infrastructure.mappers import GroupMapper

__all__ = [
    "GroupRepositoryImpl",
]


@final
class GroupRepositoryImpl(PostgresRepositoryImpl, GroupRepository):
    _mapper: GroupMapper = GroupMapper()

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        query = (
            "SELECT gr.id, gr.name, gr.university_id "
            "FROM edu_info.groups AS gr "
            "JOIN edu_info.universities AS un "
            "ON gr.university_id = un.id "
            "WHERE gr.name LIKE $1 AND un.alias = $2"
        )

        record = await self._con.fetchrow(query, name, university_alias)

        if record is None:
            return None

        return self._mapper.to_domain(record)

    async def find_by_id(self, group_id: int) -> Group | None:
        query = "SELECT * FROM edu_info.groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            return None

        return self._mapper.to_domain(record)

    async def create(self, name: str, university_id: int) -> Group:
        query = "INSERT INTO edu_info.groups (name, university_id) VALUES ($1, $2) RETURNING id"
        pk = await self._con.fetchval(query, name, university_id)

        return Group(
            id=pk,
            name=name,
            university_id=university_id,
        )

    async def find_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM edu_info.groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return self._mapper.to_domain(record)

    async def all(self) -> list[Group]:
        query = "SELECT * FROM edu_info.groups"
        records = await self._con.fetch(query)

        return [self._mapper.to_domain(**record) for record in records]
