from enum import CONTINUOUS, UNIQUE, IntEnum, verify

__all__ = [
    "UniversityId",
]


@verify(UNIQUE, CONTINUOUS)
class UniversityId(IntEnum):
    MIREA = 1
    BMSTU = 2

    @property
    def uni_name(self) -> str:
        match self.name:
            case "MIREA":
                return "РТУ МИРЭА"
            case "BMSTU":
                return "МГТУ им. Н.Э. Баумана"
            case _:
                return ""
