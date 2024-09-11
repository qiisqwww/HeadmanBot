from .bmstu_schedule_api import BMSTUScheduleAPI
from src.modules.utils.schedule_api.infrastructure.impls.mirea_schedule_api.mirea_schedule_api import MIREAScheduleAPI
from .nstu_schedule_api import NSTUScheduleAPI

__all__ = [
    "BMSTUScheduleAPI",
    "MIREAScheduleAPI",
    "NSTUScheduleAPI"
]
