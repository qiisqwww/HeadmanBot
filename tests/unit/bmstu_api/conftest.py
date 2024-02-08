from pathlib import Path
from typing import Final
from zipfile import ZipFile

import pytest
from bs4 import BeautifulSoup

ALL_SCHEDULE_PAGE_PATH: Final[Path] = Path("./tests/unit/bmstu_api/assets/bmstu_all_schedule_page.zip")

@pytest.fixture(scope="session")
def all_schedule_page() -> BeautifulSoup:
    with ZipFile(file=ALL_SCHEDULE_PAGE_PATH) as file:
        content = file.read("tests/unit/bmstu_api/assets/all_schedule_page.html")
        return BeautifulSoup(content, "html.parser")
