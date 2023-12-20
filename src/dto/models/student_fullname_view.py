from dataclasses import dataclass

from .dto import DTO
from .student import StudentId


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class StudentFullnameView(DTO):
    telegram_id: StudentId
    name: str
    surname: str
