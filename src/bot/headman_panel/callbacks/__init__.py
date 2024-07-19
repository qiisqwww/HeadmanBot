from src.bot.common import RootRouter

from .choose_student_to_downgrade_callback import include_choose_student_to_downgrade_router
from .choose_student_to_enhance_callback import include_choose_student_to_enhance_router
from .set_vice_headman_callback import include_set_vice_headman_router
from .unset_vice_headman_callback import include_unset_vice_headman_router

__all__ = [
    "include_headman_panel_callbacks_router",
]


def include_headman_panel_callbacks_router(root_router: RootRouter) -> None:
    include_set_vice_headman_router(root_router)
    include_unset_vice_headman_router(root_router)
    include_choose_student_to_enhance_router(root_router)
    include_choose_student_to_downgrade_router(root_router)
