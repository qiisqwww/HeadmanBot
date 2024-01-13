import pytest
from bs4 import BeautifulSoup

from src.modules.common.infrastructure.apis.schedule_api.impls import BmstuScheduleApi


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "group_name,exists",
    [
        ("БМТ1-13Б", True),
        ("РКТ3-91", True),
        ("ЛТ6-15Б", True),
        ("МК8-52Б", True),
        ("SOME_GROUP", False),
    ],
)
async def test_bmstu_api_group_exists(
    group_name: str, exists: bool, monkeypatch, all_schedule_soup: BeautifulSoup
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_soup

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    assert await api.group_exists(group_name) is exists
