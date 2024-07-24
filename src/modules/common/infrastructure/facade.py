from typing import Any

from src.modules.common.application import Facade, NoArgsUseCase, WithArgsUseCase
from src.modules.common.infrastructure.container import Container

__all__ = [
    "FacadeImpl",
]

class FacadeImpl(Facade):
    async def run_command_isolated(self, action_type: type[NoArgsUseCase | WithArgsUseCase], *args: Any) -> None:
        async with Container() as container:
            action = container.get_dependency(action_type)
            await action.execute(*args)
