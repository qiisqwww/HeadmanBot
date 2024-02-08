import pytest
from bs4 import BeautifulSoup

from src.modules.utils.schedule_api.infrastructure.impls import BmstuScheduleApi


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "group_name,exists",
    [
        ("БМТ1-23Б", True),
        ("РКТ3-41", True),
        ("К4-21Б", True),
        ("SOME_GROUP", False),
    ],
)
async def test_bmstu_api_group_exists(
    group_name: str, exists: bool, monkeypatch: pytest.MonkeyPatch, all_schedule_page: BeautifulSoup,
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_page

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    assert await api.group_exists(group_name) is exists
