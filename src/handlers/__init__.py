from .callback_handlers import callback_router
from .command_handlers import (
    headman_registration_router,
    headman_router,
    student_registration_router,
)

__all__ = [
    "headman_router",
    "headman_registration_router",
    "student_registration_router",
    "callback_router",
]
