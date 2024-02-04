__all__ = [
    "ScheduleApiError",
    "FailedToFetchScheduleError",
    "FailedToCheckGroupExistenceError",
    "ParsingError",
]

class ScheduleApiError(Exception):
    ...


class FailedToFetchScheduleError(ScheduleApiError):
    """Cannot fetch schedule because of internet connection."""


class FailedToCheckGroupExistenceError(ScheduleApiError):
    """Cannot check group existance because of internet connection."""

class ParsingError(ScheduleApiError):
    """Failed to parse answer from university API."""
