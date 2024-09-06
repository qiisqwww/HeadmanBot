__all__ = [
    "ScheduleApiError",
    "FailedToFetchScheduleError",
    "FailedToCheckGroupExistenceError",
    "ParsingScheduleAPIResponseError",
    "GroupNotFoundError",
    "UnexpectedScheduleDataError"
]

class ScheduleApiError(Exception):
    ...


class FailedToFetchScheduleError(ScheduleApiError):
    """Cannot fetch schedule because of internet connection."""

class GroupNotFoundError(ScheduleApiError):
    """Cannot fetch schedule because of group not found."""


class FailedToCheckGroupExistenceError(ScheduleApiError):
    """Cannot check group existance because of internet connection."""

class ParsingScheduleAPIResponseError(ScheduleApiError):
    """Failed to parse answer from university API."""

class UnexpectedScheduleDataError(ScheduleApiError):
    """Got an unexpected schedule data."""
