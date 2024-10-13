from dataclasses import dataclass

__all__ = [
    "GroupAdminInfo",
]


@dataclass(slots=True, frozen=True)
class GroupAdminInfo:
    id: int
    name: str
    headman_telegram_id: int
    headman_first_name: str
    headman_last_name: str
