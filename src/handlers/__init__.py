from src.kernel import Router

from .callbacks import choose_role_router
from .commands import start_command_router

root_router = Router(throttling=True)
root_router.include_routers(
    start_command_router,
    choose_role_router,
)

__all__ = [
    "root_router",
]
