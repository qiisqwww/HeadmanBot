from enum import Enum, auto, unique

__all__ = [
    "ProfileField",
]

@unique
class ProfileField(Enum):
    FIRST_NAME = auto()
    LAST_NAME = auto()
    BIRTHDATE = auto()
