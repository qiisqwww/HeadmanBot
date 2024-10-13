import asyncio

import uvicorn
from loguru import logger

from src.bot import init_bot_webhook
# from src.celery.worker import start_tasks_for_debug
from src.common.config import HTTP_HOST, HTTP_PORT, UVICORN_WORKERS_COUNT


def main() -> None:
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(init_bot_webhook())
    except Exception as e:
        logger.error(e)

    # if DEBUG:
    #    start_tasks_for_debug()

    try:
        uvicorn.run("src.api:app", workers=UVICORN_WORKERS_COUNT, host=HTTP_HOST, port=HTTP_PORT)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
