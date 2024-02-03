from typing import final

from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl
from src.modules.edu_info.application.repositories import EduInfoRepository


@final
class EduInfoRepositoryImpl(PostgresRepositoryImpl, EduInfoRepository):
    async def get_group_and_uni_name_by_group_id(self, group_id: int) -> tuple[str, str] | None:
        query = """SELECT gr.name AS group_name, un.name AS uni_name
                   FROM edu_info.groups AS gr
                   JOIN edu_info.universities AS un
                   ON gr.university_id = un.id
                   WHERE gr.id = $1"""
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            return None

        return record["group_name"], record["uni_name"]
