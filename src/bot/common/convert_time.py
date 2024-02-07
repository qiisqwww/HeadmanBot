from datetime import datetime, time
from zoneinfo import ZoneInfo

__all__ = [
    "convert_time_from_utc",
]


def convert_time_from_utc(utc_time: time, timezone: str) -> time:
    today = datetime.now(tz=ZoneInfo("UTC"))
    today_with_time = datetime(year=today.year, month=today.month, day=today.day,
                               hour=utc_time.hour, minute=utc_time.minute, tzinfo=ZoneInfo("UTC"))
    return today_with_time.astimezone(ZoneInfo(timezone)).time()
