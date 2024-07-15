import asyncio

import uvicorn

from src.bot import init_bot_webhook
from src.celery.worker import start_tasks_for_debug
from src.modules.common.infrastructure.config import HTTP_HOST, HTTP_PORT, UVICORN_WORKERS_COUNT, DEBUG

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_bot_webhook())

    if DEBUG:
        start_tasks_for_debug()

    uvicorn.run("src.api:app", workers=UVICORN_WORKERS_COUNT, host=HTTP_HOST, port=HTTP_PORT)
