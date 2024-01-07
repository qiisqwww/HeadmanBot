from .common import Router
from .modules import include_all_routers

__all__ = [
    "root_router",
]

root_router = Router(
    throttling=True,
)

include_all_routers(root_router)
