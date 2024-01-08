from src.bot.common.router import Router

from .registration.callbacks import include_registration_callbacks
from .registration.commands import (
    include_restart_command_router,
    include_start_command_router,
)
from .registration.finite_state import include_registration_finite_state_router

__all__ = [
    "include_student_management_router",
]


def include_student_management_router(root_router: Router) -> None:
    include_start_command_router(root_router)
    include_restart_command_router(root_router)
    include_registration_finite_state_router(root_router)
    include_registration_callbacks(root_router)
