__all__ = [
    "StudentNotFoundError",
    "CannotGrantRoleToNonStudentError",
    "CannotDowngradeNonViceHeadmanError",
]


class StudentNotFoundError(Exception):
    ...


class CannotGrantRoleToNonStudentError(Exception):
    ...


class CannotDowngradeNonViceHeadmanError(Exception):
    ...
