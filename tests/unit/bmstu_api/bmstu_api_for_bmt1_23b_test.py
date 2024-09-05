from datetime import date, time
from pathlib import Path
from typing import Final
from zoneinfo import ZoneInfo

import pytest
from pytest import MonkeyPatch

from src.modules.utils.schedule_api.domain import Schedule
from src.modules.utils.schedule_api.infrastructure.impls import BMSTUScheduleAPI

CALENDAR_PATH: Final[Path] = Path("./tests/unit/bmstu_api/assets/БМТ1-23Б.ics")
GROUP_NAME: Final[str] = "БМТ1-23Б"
MOSCOW_UTC_OFFSET: Final[int] = 3


@pytest.fixture(scope="session")
def isc_calendar() -> str:
    with CALENDAR_PATH.open() as fout:
        return fout.read()


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "day,schedule",
    [
        (
            date(year=2024, month=3, day=5),
            [
                Schedule(
                    lesson_name="Общая биология",
                    start_time=time(
                        hour=15 - MOSCOW_UTC_OFFSET,
                        minute=40,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="",
                ),
                Schedule(
                    lesson_name="Общая биология",
                    start_time=time(
                        hour=17 - MOSCOW_UTC_OFFSET,
                        minute=25,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="",
                ),
            ],
        ),
        (
            date(year=2024, month=3, day=5 + 7),
            [
                Schedule(
                    lesson_name="Общая биология",
                    start_time=time(
                        hour=15 - MOSCOW_UTC_OFFSET,
                        minute=40,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="каф. БМТ1",
                ),
                Schedule(
                    lesson_name="Общая биология",
                    start_time=time(
                        hour=17 - MOSCOW_UTC_OFFSET,
                        minute=25,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="",
                ),
            ],
        ),
        (
            date(year=2024, month=3, day=6),
            [
                Schedule(
                    lesson_name="Химия",
                    start_time=time(
                        hour=8 - MOSCOW_UTC_OFFSET,
                        minute=30,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="327.1",
                ),
                Schedule(
                    lesson_name="Химия",
                    start_time=time(
                        hour=10 - MOSCOW_UTC_OFFSET,
                        minute=15,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="каф. ФН5",
                ),
                Schedule(
                    lesson_name="Элективный курс по физической культуре и спорту",
                    start_time=time(
                        hour=12 - MOSCOW_UTC_OFFSET,
                        minute=00,
                        tzinfo=ZoneInfo("UTC"),
                    ),
                    classroom="каф. ФВ",
                ),
            ],
        ),
    ],
)
async def test_fetch_bmt1_23b_schedule(
    day: date,
    schedule: list[Schedule],
    monkeypatch: MonkeyPatch,
    isc_calendar: str,
) -> None:
    api = BMSTUScheduleAPI()

    async def fetch_isc(*_) -> str:
        return isc_calendar

    monkeypatch.setattr(api, "_fetch_isc", fetch_isc)
    fetched_schedule = await api.fetch_schedule(GROUP_NAME, day=day)
    assert frozenset(fetched_schedule) == frozenset(schedule)
