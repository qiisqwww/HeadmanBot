from .common import RootRouter
from .modules import include_all_routers

__all__ = [
    "root_router",
]

root_router = RootRouter(throttling=True)

include_all_routers(root_router)
