__all__ = [
    "FailedToFetchScheduleException",
    "FailedToCheckGroupExistence",
]


class FailedToFetchScheduleException(Exception):
    """Cannot fetch schedule because of internet connection."""


class FailedToCheckGroupExistence(Exception):
    """Cannot check group existance because of internet connection."""
