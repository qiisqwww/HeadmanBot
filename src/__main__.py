import asyncio

import uvicorn

from src.api import app
from src.bot import bot
from src.modules.common.infrastructure import HTTP_HOST, HTTP_PORT, configure_logger
from src.modules.common.infrastructure.build_scheduler import build_scheduler
from src.modules.common.infrastructure.container import Container


async def main() -> None:
    configure_logger()

    await Container.init(bot)
    scheduler = await build_scheduler(bot)
    scheduler.start()

    server_config = uvicorn.Config(app, host=HTTP_HOST, port=HTTP_PORT)
    server = uvicorn.Server(server_config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
