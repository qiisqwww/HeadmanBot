__all__ = [
    "NotFoundGroupError"
]


class NotFoundGroupError(Exception):
    """Raise if administrator is trying to delete student from group
    that not exists"""
