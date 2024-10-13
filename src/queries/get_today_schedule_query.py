from injector import inject

from src.common import UseCase
from src.modules.attendance.application.repositories import LessonRepository
from src.modules.attendance.domain import Lesson


class GetTodayScheduleQuery(UseCase):
    _repository: LessonRepository

    @inject
    def __init__(self, repository: LessonRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> list[Lesson]:
        return await self._repository.filter_by_group_id(group_id)
