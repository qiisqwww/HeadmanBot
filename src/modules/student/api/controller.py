from src.kernel import Router
from src.modules.student.internal.controllers import (
    access_callback_router,
    registered_commands_router,
    registration_callbacks_router,
    registration_commands_router,
    registration_finite_state_router,
)

__all__ = [
    "student_router",
]

student_router = Router()
student_router.include_routers(
    registration_commands_router,
    registered_commands_router,
    registration_callbacks_router,
    registration_finite_state_router,
    access_callback_router,
)
