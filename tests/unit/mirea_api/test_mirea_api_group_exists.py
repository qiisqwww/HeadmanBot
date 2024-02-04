
import pytest

from src.modules.utils.schedule_api.infrastructure.impls import MireaScheduleApi


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "group_name,exists",
    [
        ("ИКБО-40-23", True),
        ("ИКБО-44-23", True),
        ("SOME_GROUP", False),
        ("ИКБО-49-23", False),
    ],
)
async def test_mirea_api_group_exists(group_name: str, exists: bool) -> None:
    api = MireaScheduleApi()
    assert await api.group_exists(group_name) == exists
