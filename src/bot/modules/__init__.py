from src.bot.common.router import RootRouter

from .attendance.attendance_router import include_attendance_router
from .help import include_help_command_router
from .student_management.student_management_router import (
    include_student_management_router,
)

__all__ = [
    "include_all_routers",
]


def include_all_routers(root_router: RootRouter) -> None:
    include_help_command_router(root_router)
    include_student_management_router(root_router)
    include_attendance_router(root_router)
