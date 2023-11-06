from ..dto import University
from .base import Service


class UniversityService(Service):
    async def all(self) -> list[University]:
        query = "SELECT * FROM universities"
        records = await self._con.fetch(query)

        return [University.from_record(record) for record in records]
