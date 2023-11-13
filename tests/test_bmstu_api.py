import pytest

from src.api.bmstu_schedule_api import BmstuScheduleApi

# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "group_name,exists",
#     [
#         ("БМТ1-13Б", True),
#         ("РКТ3-91", True),
#         ("SOME_GROUP", False),
#     ],
# )
# async def test_bmstu_api_group_exists(group_name: str, exists: bool) -> None:
#     api = BmstuScheduleApi()
#     assert await api.group_exists(group_name) == exists


@pytest.mark.asyncio
async def test_bmstu_api_fetch_schedule() -> None:
    api = BmstuScheduleApi()
    print(await api.fetch_schedule("БМТ1-13Б"))
    assert True
