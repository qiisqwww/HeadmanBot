from aiogram.filters.callback_data import CallbackData

__all__ = [
    "GroupsListCallbackData",
]


class GroupsListCallbackData(CallbackData, prefix="get_list_of_groups_and_their_headman"):  # type: ignore
    ...
