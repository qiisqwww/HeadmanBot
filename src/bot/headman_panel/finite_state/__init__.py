from src.bot.common.router.root_router import RootRouter

from .set_vice_headman import set_vice_headman_router
from .unset_vice_headman import unset_vice_headman_router

__all__ = [
    "include_headman_panel_finite_state",
]


def include_headman_panel_finite_state(root_router: RootRouter) -> None:
    root_router.include_router(set_vice_headman_router)
    root_router.include_router(unset_vice_headman_router)
