from .common import Router
from .help import help_command_router

__all__ = [
    "root_router",
]

root_router = Router(
    throttling=True,
)

root_router.include_routers(
    help_command_router,
)
