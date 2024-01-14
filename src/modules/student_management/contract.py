from abc import abstractmethod
from typing import Any

from src.modules.common.application import Dependency


class StudentManagementContract(Dependency):
    @abstractmethod
    async def get_students_info(self, group_id: int) -> list[dict[str, Any]]:
        """Return data in format like
        student_info = return_value[0]

        student_info['id']: int -> student id
        student_info['telegram_id']: int -> student telegram id
        student_info['name']: str -> student name
        student_info['surname']: str -> student surname
        student_info['is_checked_in_today']: bool -> True mean, that student already have checked in today.
        """
