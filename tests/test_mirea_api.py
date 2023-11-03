import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from src.mirea_api import MireaScheduleApi

from .assets import PARSE_RESULT

JSON_PATH: Path = Path("./tests/assets/mirea_api_response_with_schedule.json")
GROUP_NAME: str = "ИКБО-40-23"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class MockResponse:
    @staticmethod
    def json():
        with open(JSON_PATH) as json_data:
            return json.loads(json_data.read())


def test_mirea_api_parsing() -> None:
    api = MireaScheduleApi()

    for day in daterange(datetime(year=2023, month=10, day=1), datetime(year=2023, month=10, day=31)):
        assert api._parse_schedule(MockResponse().json(), day) == PARSE_RESULT[day]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "group_name,exists",
    [
        ("ИКБО-40-23", True),
        ("SOME_GROUP", False),
    ],
)
async def test_mirea_api_group_exists(group_name: str, exists: bool) -> None:
    api = MireaScheduleApi()
    assert await api.group_exists(group_name) == exists
