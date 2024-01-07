from src.bot.common.router import Router

from .help import include_help_command_router
from .student_management.student_management_router import (
    include_student_management_router,
)

__all__ = [
    "include_all_routers",
]


def include_all_routers(root_router: Router) -> None:
    include_help_command_router(root_router)
    include_student_management_router(root_router)
