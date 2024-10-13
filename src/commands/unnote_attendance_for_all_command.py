from typing import final

from src.common.database import DbContext
from src.common.use_case import NoArgsUseCase
from src.repositories import StudentRepository

__all__ = [
    "UnnoteAttendanceForAllCommand",
]


@final
class UnnoteAttendanceForAllCommand(NoArgsUseCase):
    _repository: StudentRepository

    def __init__(self, con: DbContext) -> None:
        self._repository = StudentRepository(con)

    async def execute(self) -> None:
        await self._repository.update_attendance_noted_all(False)
