import asyncio

import uvicorn

from src.api import app
from src.modules.common.infrastructure import (
    HTTP_HOST,
    HTTP_PORT,
    configurate_logger,
    init_database,
)

# async def init_jobs(bot: Bot, pool: Pool) -> None:
#     sender = SendingJob(bot, pool)
#     database_updater = UpdateDatabaseJob(pool)
#
#     await database_updater.start()
#     await sender.start()


async def main() -> None:
    configurate_logger()

    await init_database()
    # await init_jobs(bot, pool)

    server_config = uvicorn.Config(app, host=HTTP_HOST, port=HTTP_PORT)
    server = uvicorn.Server(server_config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
