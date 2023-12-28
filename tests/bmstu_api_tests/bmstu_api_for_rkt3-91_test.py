from datetime import time

import pytest
from bs4 import BeautifulSoup

from src.external.apis.schedule_api.dto import Schedule
from src.external.apis.schedule_api.enums import Weekday
from src.external.apis.schedule_api.impls import BmstuScheduleApi


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weekday,expected_schedule",
    [
        (
            Weekday.MONDAY,
            [
                Schedule("Основы компьютерного проектирования", time.fromisoformat("12:00")),
                Schedule("Технология инструментального производства", time.fromisoformat("13:50")),
                Schedule("Технология инструментального производства", time.fromisoformat("15:40")),
            ],
        ),
        (
            Weekday.TUESDAY,
            [],
        ),
        (
            Weekday.WEDNESDAY,
            [
                Schedule("Практика", time.fromisoformat("12:00")),
            ],
        ),
        (
            Weekday.THURSDAY,
            [
                Schedule("Организация и планирование производства", time.fromisoformat("12:00")),
                Schedule("Сверхтвердые материалы, технология и особенности эксплуатации", time.fromisoformat("13:50")),
                Schedule("Станки инструментального производства", time.fromisoformat("15:40")),
                Schedule("Станки инструментального производства", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.FRIDAY,
            [
                Schedule("Основы проектирования режущих инструментов", time.fromisoformat("10:15")),
                Schedule("Основы проектирования режущих инструментов", time.fromisoformat("12:00")),
                Schedule("Технология инструментального производства", time.fromisoformat("13:50")),
            ],
        ),
        (
            Weekday.SATURDAY,
            [
                Schedule("Самостоятельная работа", time.fromisoformat("12:00")),
            ],
        ),
        (Weekday.SUNDAY, []),
    ],
)
async def test_bmstu_api_fetch_schedule_rkt3_91(
    all_schedule_soup: BeautifulSoup,
    rkt3_91_scheule_soup: BeautifulSoup,
    monkeypatch,
    weekday: Weekday,
    expected_schedule: list[Schedule],
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_soup

    async def fetch_schedule_soup(*args, **kwargs) -> BeautifulSoup:
        return rkt3_91_scheule_soup

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    monkeypatch.setattr(api, "_fetch_schedule_soup", fetch_schedule_soup)

    schedule = await api.fetch_schedule("РКТ3-91", weekday)

    assert schedule == expected_schedule


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weekday,expected_schedule",
    [
        (
            Weekday.MONDAY,
            [
                Schedule("Основы компьютерного проектирования", time.fromisoformat("10:15")),
                Schedule("Основы компьютерного проектирования", time.fromisoformat("12:00")),
                Schedule("Технология инструментального производства", time.fromisoformat("13:50")),
                Schedule("Технология инструментального производства", time.fromisoformat("15:40")),
            ],
        ),
        (
            Weekday.TUESDAY,
            [],
        ),
        (
            Weekday.WEDNESDAY,
            [
                Schedule("Практика", time.fromisoformat("12:00")),
            ],
        ),
        (
            Weekday.THURSDAY,
            [
                Schedule("Сверхтвердые материалы, технология и особенности эксплуатации", time.fromisoformat("12:00")),
                Schedule("Сверхтвердые материалы, технология и особенности эксплуатации", time.fromisoformat("13:50")),
                Schedule("Станки инструментального производства", time.fromisoformat("15:40")),
                Schedule("Станки инструментального производства", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.FRIDAY,
            [
                Schedule("Основы проектирования режущих инструментов", time.fromisoformat("10:15")),
                Schedule("Основы проектирования режущих инструментов", time.fromisoformat("12:00")),
                Schedule("Основы проектирования режущих инструментов", time.fromisoformat("13:50")),
            ],
        ),
        (
            Weekday.SATURDAY,
            [
                Schedule("Самостоятельная работа", time.fromisoformat("12:00")),
            ],
        ),
        (Weekday.SUNDAY, []),
    ],
)
async def test_bmstu_api_fetch_schedule_rkt3_91_not_zn(
    all_schedule_soup: BeautifulSoup,
    rkt3_91_scheule_soup: BeautifulSoup,
    monkeypatch,
    weekday: Weekday,
    expected_schedule: list[Schedule],
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_soup

    async def fetch_schedule_soup(*args, **kwargs) -> BeautifulSoup:
        return rkt3_91_scheule_soup

    def is_zn(*args, **kwargs) -> bool:
        return False

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    monkeypatch.setattr(api, "_fetch_schedule_soup", fetch_schedule_soup)
    monkeypatch.setattr(api, "_is_zn", is_zn)

    schedule = await api.fetch_schedule("РКТ3-91", weekday)

    assert schedule == expected_schedule
