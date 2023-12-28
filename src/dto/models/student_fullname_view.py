from dataclasses import dataclass

from .model import Model
from .student import StudentId


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class StudentFullnameView(Model):
    telegram_id: StudentId
    name: str
    surname: str
