from typing import final

from src.modules.edu_info.application.repositories import GroupInfoRepository
from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl
from src.modules.edu_info.domain import GroupInfo

from ..mappers import GroupInfoMapper

__all__ = [
    "GroupInfoRepositoryImpl",
]


@final
class GroupInfoRepositoryImpl(PostgresRepositoryImpl, GroupInfoRepository):
    _mapper: GroupInfoMapper = GroupInfoMapper()

    async def fetch_all(self) -> list[GroupInfo]:
        query = """SELECT gr.id, gr.name, uni.alias
                    FROM edu_info.groups AS gr 
                    JOIN edu_info.universities AS uni 
                    ON gr.university_id = uni.id"""
        records = await self._con.fetch(query)

        return [self._mapper.to_domain(record) for record in records]
