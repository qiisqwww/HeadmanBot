from typing import final

from src.modules.edu_info.domain.models import Group, GroupAdminInfo

__all__ = [
    "GroupAdminInfoMapper",
]


@final
class GroupAdminInfoMapper:
    def to_domain(self, group: Group, headman: dict) -> GroupAdminInfo:
        return GroupAdminInfo(
            id=group.id,
            name=group.name,
            headman_telegram_id=headman["telegram_id"],
            headman_first_name=headman["first_name"],
            headman_last_name=headman["last_name"],
        )
