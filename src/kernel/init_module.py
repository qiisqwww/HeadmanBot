import src.kernel.config as config
from src.kernel.protocols import FindStudentServiceProtocol

__all__ = [
    "init_kernel",
]


def init_kernel(find_student_service: type[FindStudentServiceProtocol]) -> None:
    config.config.FIND_USER_SERVICE = find_student_service
