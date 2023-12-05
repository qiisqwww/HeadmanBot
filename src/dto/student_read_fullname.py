from dataclasses import dataclass

from src.dto import StudentId

from .dto import DTO


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class StudentReadFullname(DTO):
    student_id: StudentId
    name: str
    surname: str
