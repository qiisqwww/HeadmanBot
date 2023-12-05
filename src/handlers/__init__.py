from src.kernel import Router

from .commands import start_command_router

root_router = Router(throttling=True)
root_router.include_routers(
    start_command_router,
)

__all__ = [
    "root_router",
]
