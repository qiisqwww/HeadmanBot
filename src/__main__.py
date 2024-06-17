import asyncio

import uvicorn
from celery.schedules import crontab

from src.bot import init_bot_webhook
from src.celery.worker import make_attendance_relevant, worker
from src.modules.common.infrastructure.config import DEBUG, HTTP_HOST, HTTP_PORT, UVICORN_WORKERS_COUNT

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_bot_webhook())
    if DEBUG:
        make_attendance_relevant.delay()
    else:
        worker.conf.beat_schedule = {
            "make_attendance_relevant": {
                "task": "tasks.make_attendance_relevant",
                "schedule": crontab(
                    hour="1",
                    minute="0",
                    day_of_week="mon-sun",
                ),
            },
        }

    uvicorn.run("src.api:app", workers=UVICORN_WORKERS_COUNT, host=HTTP_HOST, port=HTTP_PORT)
