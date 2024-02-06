from typing import final
from datetime import date

from injector import inject

from src.modules.common.application import UseCase
from src.modules.student_management.application.repositories import StudentRepository
from src.modules.student_management.domain.enums import ProfileField

__all__ = [
    "EditProfileFieldByNameCommand"
]


@final
class EditProfileFieldByNameCommand(UseCase):
    _repository: StudentRepository

    @inject
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    async def execute(
            self,
            field_type: ProfileField,
            new_data: str | None | date,
            student_id: int
    ) -> None:
        if field_type == ProfileField.NAME:
            await self._repository.update_name_by_id(
                student_id=student_id,
                new_name=new_data
            )
        if field_type == ProfileField.SURNAME:
            await self._repository.update_surname_by_id(
                student_id=student_id,
                new_surname=new_data
            )
        if field_type == ProfileField.BIRTHDATE:
            await self._repository.update_birthdate_by_id(
                student_id=student_id,
                new_date=new_data
            )
