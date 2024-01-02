from src.presentation.common.router import Router

from .registration.callbacks import choose_role_router, choose_university_router
from .registration.commands import restart_command_router, start_command_router
from .registration.finite_state import registration_finite_state_router

__all__ = [
    "student_management_router",
]

student_management_router = Router()

student_management_router.include_routers(
    start_command_router,
    restart_command_router,
    choose_role_router,
    choose_university_router,
    registration_finite_state_router,
)
