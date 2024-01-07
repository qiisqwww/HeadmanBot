from src.bot.common.router import Router

# from .registration.callbacks import (
#     ask_new_fullname_validity_router,
#     choose_role_router,
#     choose_university_router,
# )
# from .registration.finite_state import registration_finite_state_router
from .registration.commands import (
    include_restart_command_router,
    include_start_command_router,
)

__all__ = [
    "include_student_management_router",
]


def include_student_management_router(root_router: Router) -> None:
    include_start_command_router(root_router)
    include_restart_command_router(root_router)
