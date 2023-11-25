from enum import EnumMeta

__all__ = [
    "EnumContainsMeta",
]


class EnumContainsMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)

        except ValueError:
            return False

        return True
