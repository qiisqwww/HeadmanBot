import asyncio

import uvicorn

from src.bot import init_bot_webhook
from src.modules.common.infrastructure.config import HTTP_HOST, HTTP_PORT, UVICORN_WORKERS_COUNT

if __name__ == "__main__":
    asyncio.run(init_bot_webhook())
    uvicorn.run("src.api:app", workers=UVICORN_WORKERS_COUNT, host=HTTP_HOST, port=HTTP_PORT)
