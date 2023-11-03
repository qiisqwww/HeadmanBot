import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

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


def test_mirea_api(monkeypatch) -> None:
    def fake_get(_: str) -> MockResponse:
        return MockResponse()

    api = MireaScheduleApi()
    monkeypatch.setattr(requests, "get", fake_get)

    for day in daterange(datetime(year=2023, month=10, day=1), datetime(year=2023, month=10, day=31)):
        assert api.get_schedule(GROUP_NAME, day) == PARSE_RESULT[day]
