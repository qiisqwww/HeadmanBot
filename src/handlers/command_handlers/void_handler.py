from aiogram import Router

__all__ = [
    "void_router",
]


void_router = Router()


@void_router.message(flags={"void": "void"})
async def handles_everything() -> None:
    pass
