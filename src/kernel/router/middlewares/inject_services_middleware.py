from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.repositories.impls import (
    AttendanceRepositoryImpl,
    GroupRepositoryImpl,
    LessonRepositoryImpl,
    StudentRepositoryImpl,
    UniversityRepositoryImpl,
)
from src.services import (
    AttendanceService,
    GroupService,
    LessonService,
    RegistrationService,
    Service,
    StudentService,
    UniversityService,
)
from src.services.impls import (
    AttendanceServiceImpl,
    GroupServiceImpl,
    LessonServiceImpl,
    RegistrationServiceImpl,
    StudentServiceImpl,
    UniversityServiceImpl,
)
from src.services.impls.redis_service import RedisService

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectServices",
    "ServiceClass",
]

ServiceClass: TypeAlias = type[Service]


class InjectServices(BaseMiddleware):
    _deps: dict[str, ServiceClass]

    def __init__(self, **deps: ServiceClass) -> None:
        self._deps = deps

    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        con = data["postgres_con"]

        group_repository = GroupRepositoryImpl(con)
        university_repository = UniversityRepositoryImpl(con)
        lesson_repository = LessonRepositoryImpl(con)
        student_repository = StudentRepositoryImpl(con)
        attendance_repository = AttendanceRepositoryImpl(con)

        group_service = GroupServiceImpl(group_repository)
        university_service = UniversityServiceImpl(university_repository)
        lesson_service = LessonServiceImpl(lesson_repository, group_service, university_service)
        student_service = StudentServiceImpl(student_repository)
        attendance_service = AttendanceServiceImpl(attendance_repository, lesson_service, student_service)
        registration_service = RegistrationServiceImpl(
            student_repository, attendance_service, group_service, university_service
        )

        for service_obj_name, service_class in self._deps.items():
            if issubclass(service_class, RedisService):
                data[service_obj_name] = service_class(data["redis_con"])

            elif issubclass(service_class, GroupService):
                data[service_obj_name] = group_service

            elif issubclass(service_class, LessonService):
                data[service_obj_name] = lesson_service

            elif issubclass(service_class, UniversityService):
                data[service_obj_name] = university_service

            elif issubclass(service_class, StudentService):
                data[service_obj_name] = student_service

            elif issubclass(service_class, RegistrationService):
                data[service_obj_name] = registration_service

            elif issubclass(service_class, AttendanceService):
                data[service_obj_name] = attendance_service

            else:
                raise TypeError("Unknown service type, may be you want register it?")

        return await handler(event, data)
