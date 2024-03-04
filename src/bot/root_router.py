from .common import RootRouter
from .help import include_help_command_router
from .poll_attendance import include_poll_attendance_routers
from .profile import include_profile_router
from .registration import include_registration_routers
from .show_group_attendance import include_show_group_attendance_routers
from .show_schedule import include_get_schedule_command

__all__ = [
    "build_root_router",
]


def build_root_router() -> RootRouter:
    root_router = RootRouter(throttling=True)

    include_registration_routers(root_router)
    include_help_command_router(root_router)
    include_poll_attendance_routers(root_router)
    include_show_group_attendance_routers(root_router)
    include_profile_router(root_router)
    include_get_schedule_command(root_router)

    return root_router
