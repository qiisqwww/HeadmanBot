from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .async_job import AsyncJob

__all__ = [
    "AsyncScheduler",
]


class AsyncScheduler:
    _scheduler: AsyncIOScheduler

    def __init__(self, *jobs: AsyncJob) -> None:
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        for job in jobs:
            self._scheduler.add_job(self._job_wrapper(job), trigger=job.trigger, **job.trigger_args)

    @staticmethod
    def _job_wrapper(job: AsyncJob):
        """APScheduler don't support async callable object and this wrapper solve this problem."""

        async def _job_wrapper_inner():
            await job()

        return _job_wrapper_inner

    def start(self) -> None:
        self._scheduler.start()
