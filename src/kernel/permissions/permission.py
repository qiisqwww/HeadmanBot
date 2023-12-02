from enum import IntEnum

__all__ = [
    "Permission",
]


class Permission(IntEnum):
    NON_REGISTERED = 0
    REGISTRED = 1
