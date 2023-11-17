import pytest
from bs4 import BeautifulSoup

ALL_SCHEDULE_PATH: str = "./tests/assets/bmstu/full_schedule.html"
BMT1_13B_SCHEDULE_PATH: str = "./tests/assets/bmstu/bmt1-13b_week_schedule.html"
RKT3_91_SCHEDULE_PATH: str = "./tests/assets/bmstu/rkt3-91.html"


@pytest.fixture(scope="session")
def all_schedule_soup() -> BeautifulSoup:
    with open(ALL_SCHEDULE_PATH) as html:
        return BeautifulSoup(html.read(), "html.parser")


@pytest.fixture(scope="session")
def bmt1_13b_scheule_soup() -> BeautifulSoup:
    with open(BMT1_13B_SCHEDULE_PATH) as html:
        return BeautifulSoup(html.read(), "html.parser")


@pytest.fixture(scope="session")
def rkt3_91_scheule_soup() -> BeautifulSoup:
    with open(RKT3_91_SCHEDULE_PATH) as html:
        return BeautifulSoup(html.read(), "html.parser")
