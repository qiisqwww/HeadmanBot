__all__ = [
    "NotFoundStudentError"
]


class NotFoundStudentError(Exception):
    """Raise if administrator is trying to delete student who not exists"""
