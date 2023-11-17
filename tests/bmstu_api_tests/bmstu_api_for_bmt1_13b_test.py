from datetime import time

import pytest
from bs4 import BeautifulSoup

from src.api.bmstu_schedule_api import BmstuScheduleApi
from src.dto.schedule import Schedule
from src.enums.weekday import Weekday


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weekday,expected_schedule",
    [
        (
            Weekday.MONDAY,
            [
                Schedule("Физическая культура и спорт", time.fromisoformat("12:00")),
                Schedule("Математический анализ", time.fromisoformat("15:40")),
                Schedule("Аналитическая геометрия", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.TUESDAY,
            [
                Schedule("Начертательная геометрия", time.fromisoformat("12:00")),
                Schedule("Аналитическая геометрия", time.fromisoformat("13:50")),
                Schedule("История России", time.fromisoformat("15:40")),
                Schedule("Физическая культура и спорт", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.WEDNESDAY,
            [
                Schedule("Алгоритмизация и программирование", time.fromisoformat("08:30")),
                Schedule("Алгоритмизация и программирование", time.fromisoformat("10:15")),
                Schedule("Начертательная геометрия", time.fromisoformat("12:00")),
            ],
        ),
        (
            Weekday.THURSDAY,
            [
                Schedule("Общая биология", time.fromisoformat("10:15")),
                Schedule("Общая биология", time.fromisoformat("12:00")),
            ],
        ),
        (
            Weekday.FRIDAY,
            [
                Schedule("Иностранный язык", time.fromisoformat("13:50")),
                Schedule(
                    "Математические основы информатики Часть 1: математическая логика и теория алгоритмов",
                    time.fromisoformat("15:40"),
                ),
            ],
        ),
        (
            Weekday.SATURDAY,
            [
                Schedule("Математический анализ", time.fromisoformat("13:50")),
                Schedule("История России", time.fromisoformat("15:40")),
            ],
        ),
        (Weekday.SUNDAY, []),
    ],
)
async def test_bmstu_api_fetch_schedule_bmt13(
    all_schedule_soup: BeautifulSoup,
    bmt1_13b_scheule_soup: BeautifulSoup,
    monkeypatch,
    weekday: Weekday,
    expected_schedule: list[Schedule],
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_soup

    async def fetch_schedule_soup(*args, **kwargs) -> BeautifulSoup:
        return bmt1_13b_scheule_soup

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    monkeypatch.setattr(api, "_fetch_schedule_soup", fetch_schedule_soup)

    schedule = await api.fetch_schedule("БМТ1-13Б", weekday)

    assert schedule == expected_schedule


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weekday,expected_schedule",
    [
        (
            Weekday.MONDAY,
            [
                Schedule("Физическая культура и спорт", time.fromisoformat("12:00")),
                Schedule("Математический анализ", time.fromisoformat("15:40")),
                Schedule("Аналитическая геометрия", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.TUESDAY,
            [
                Schedule("Начертательная геометрия", time.fromisoformat("12:00")),
                Schedule("Аналитическая геометрия", time.fromisoformat("13:50")),
                Schedule("Физическая культура и спорт", time.fromisoformat("17:25")),
            ],
        ),
        (
            Weekday.WEDNESDAY,
            [
                Schedule("Алгоритмизация и программирование", time.fromisoformat("08:30")),
                Schedule("Алгоритмизация и программирование", time.fromisoformat("10:15")),
                Schedule("Начертательная геометрия", time.fromisoformat("12:00")),
            ],
        ),
        (
            Weekday.THURSDAY,
            [
                Schedule("Общая биология", time.fromisoformat("08:30")),
                Schedule("Общая биология", time.fromisoformat("10:15")),
            ],
        ),
        (
            Weekday.FRIDAY,
            [
                Schedule("Иностранный язык", time.fromisoformat("13:50")),
                Schedule(
                    "Математические основы информатики Часть 1: математическая логика и теория алгоритмов",
                    time.fromisoformat("15:40"),
                ),
                Schedule(
                    "Математические основы информатики Часть 1: математическая логика и теория алгоритмов",
                    time.fromisoformat("17:25"),
                ),
            ],
        ),
        (
            Weekday.SATURDAY,
            [
                Schedule("Математический анализ", time.fromisoformat("12:00")),
                Schedule("Математический анализ", time.fromisoformat("13:50")),
                Schedule("История России", time.fromisoformat("15:40")),
            ],
        ),
        (Weekday.SUNDAY, []),
    ],
)
async def test_bmstu_api_fetch_schedule_bmt13_not_zn(
    all_schedule_soup: BeautifulSoup,
    bmt1_13b_scheule_soup: BeautifulSoup,
    monkeypatch,
    weekday: Weekday,
    expected_schedule: list[Schedule],
) -> None:
    async def fetch_all_schedule_soup_stub(*args, **kwargs) -> BeautifulSoup:
        return all_schedule_soup

    async def fetch_schedule_soup(*args, **kwargs) -> BeautifulSoup:
        return bmt1_13b_scheule_soup

    def is_zn(*args, **kwargs) -> bool:
        return False

    api = BmstuScheduleApi()
    monkeypatch.setattr(api, "_fetch_all_schedule_soup", fetch_all_schedule_soup_stub)
    monkeypatch.setattr(api, "_fetch_schedule_soup", fetch_schedule_soup)
    monkeypatch.setattr(api, "_is_zn", is_zn)

    schedule = await api.fetch_schedule("БМТ1-13Б", weekday)

    assert schedule == expected_schedule
