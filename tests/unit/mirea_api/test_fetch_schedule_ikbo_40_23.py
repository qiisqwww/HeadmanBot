from datetime import UTC, datetime, time
from pathlib import Path
from typing import Final

import pytest
from pytest import MonkeyPatch

from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.impls.mirea_schedule_api import MireaScheduleApi

CALENDAR_PATH: Final[Path] = Path("./tests/unit/mirea_api/assets/ИКБО-40-23.ics")
GROUP_NAME: Final[str] = "ИКБО-40-23"

@pytest.fixture(scope="session")
def isc_calendar() -> str:
    with CALENDAR_PATH.open() as fout:
        return fout.read()


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "day,schedule",
    [
        (datetime(year=2023, month=12, day=25, tzinfo=UTC), [
           Schedule(lesson_name="Зачет Основы российской государственности",
                    start_time=time(hour=10, minute=40)),
           Schedule(lesson_name="Зачет История России",
                    start_time=time(hour=14, minute=20)),
           ]),
    ],
)
async def test_fetch_ikbo_40_23_schedule(day: datetime, schedule: list[Schedule], monkeypatch: MonkeyPatch, isc_calendar: str) -> None:
    api = MireaScheduleApi()

    async def fetch_isc(*_) -> str:
        return isc_calendar

    monkeypatch.setattr(api, "_fetch_isc", fetch_isc)
    fetched_schedule = await api.fetch_schedule(GROUP_NAME, day=day)
    assert frozenset(fetched_schedule) == frozenset(schedule)
