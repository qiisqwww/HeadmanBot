from datetime import date, time
from pathlib import Path
from typing import Final
from zoneinfo import ZoneInfo

import pytest
from pytest import MonkeyPatch

from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.impls.mirea_schedule_api import MireaScheduleApi

CALENDAR_PATH: Final[Path] = Path("./tests/unit/mirea_api/assets/ИКБО-40-23.ics")
GROUP_NAME: Final[str] = "ИКБО-40-23"
MOSCOW_UTC_OFFSET: Final[int] = 3

@pytest.fixture()
def isc_calendar() -> str:
    with CALENDAR_PATH.open() as fout:
        return fout.read()

@pytest.fixture()
def isc_location() -> bytes:
    return '{"data":[{"id":741,"targetTitle":"ИКБО-40-23","fullTitle":"ИКБО-40-23","scheduleTarget":1,"iCalLink":"https://schedule-of.mirea.ru/schedule/api/ical/1/741","scheduleImageLink":"https://schedule-of.mirea.ru/schedule/genericschedule?type=1&id=741&asImage=True","scheduleUpdateImageLink":"https://schedule-of.mirea.ru/schedule/genericupdate?type=1&id=741&asImage=True"}],"nextPageToken":null}'.encode()


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "day,schedule",
    [
        (date(year=2023, month=12, day=25), [
           Schedule(lesson_name="Зачет Основы российской государственности",
                    start_time=time(hour=10 - MOSCOW_UTC_OFFSET, minute=40, tzinfo=ZoneInfo("UTC"))),
           Schedule(lesson_name="Зачет История России",
                    start_time=time(hour=14 - MOSCOW_UTC_OFFSET, minute=20, tzinfo=ZoneInfo("UTC"))),
           ]),
    ],
)
async def test_fetch_ikbo_40_23_schedule(day: date, schedule: list[Schedule], monkeypatch: MonkeyPatch, isc_calendar: str, isc_location: bytes) -> None:
    api = MireaScheduleApi()

    async def fetch_isc(*_) -> str:
        return isc_calendar

    async def fetch_isc_location(*_) -> bytes:
        return isc_location

    monkeypatch.setattr(api, "_fetch_isc", fetch_isc)
    monkeypatch.setattr(api, "_fetch_isc_link_location", fetch_isc_location)

    fetched_schedule = await api.fetch_schedule(GROUP_NAME, day=day)
    assert frozenset(fetched_schedule) == frozenset(schedule)
