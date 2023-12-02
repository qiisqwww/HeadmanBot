from enum import UNIQUE, EnumMeta, StrEnum, verify

__all__ = [
    "Role",
]


class EnumContainsMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)

        except ValueError:
            return False

        return True


@verify(UNIQUE)
class Role(StrEnum, metaclass=EnumContainsMeta):
    ADMIN = "Админ"
    HEADMAN = "Староста"
    VICE_HEADMAN = "Заместитель Старосты"
    STUDENT = "Студент"
