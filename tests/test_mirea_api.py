import json
from pathlib import Path
from typing import Any

import pytest

JSON_PATH: Path = Path("./tests/assets/mirea_api_response_with_schedule.json")


@pytest.fixture(scope="session")
def api_json() -> dict[str, Any]:
    with open(JSON_PATH) as json_file:
        return json.load(json_file)


# def test_mirea_api_parsing() -> None:
#     api = MireaScheduleApi()
#
#     for day in daterange(datetime(year=2023, month=10, day=1), datetime(year=2023, month=10, day=31)):
#         assert api._parse_schedule(MockResponse().json(), day) == PARSE_RESULT[day]


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "group_name,exists",
#     [
#         ("ИКБО-40-23", True),
#         ("ИКБО-44-23", True),
#         ("SOME_GROUP", False),
#         ("ИКБО-49-23", False),
#     ],
# )
# async def test_mirea_api_group_exists(group_name: str, exists: bool) -> None:
#     api = MireaScheduleApi()
#     assert await api.group_exists(group_name) == exists
