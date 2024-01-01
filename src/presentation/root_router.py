from .common import Router
from .help import help_command_router
from .student_management.student_management_router import student_management_router

__all__ = [
    "root_router",
]

root_router = Router(
    throttling=True,
)

root_router.include_routers(
    help_command_router,
    student_management_router,
)
