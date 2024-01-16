from src.bot import bot
from src.bot.common.jobs import AsyncScheduler
from src.bot.modules.attendance.jobs import SendingJob
from src.modules.common.infrastructure.config.config import DEBUG
from src.modules.common.infrastructure.database import get_postgres_pool

__all__ = [
    "build_scheduler",
]


async def build_scheduler() -> AsyncScheduler:
    pool = await get_postgres_pool()
    sending_job = SendingJob(bot, pool, DEBUG)

    return AsyncScheduler(
        sending_job,
    )
