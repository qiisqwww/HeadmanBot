from .headman_commands import headman_router
from .headman_registration_commands import headman_registration_router
from .student_registration_command import student_registration_router

__all__ = [
    "headman_router",
    "headman_registration_router",
    "student_registration_router",
]
