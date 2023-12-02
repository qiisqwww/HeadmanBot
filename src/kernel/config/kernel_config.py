from src.kernel.protocols import FindStudentServiceProtocol

from .exceptions import AlreadyInitializedConfig, UninitializedConfig

__all__ = [
    "KernelConfig",
]


class KernelConfig:
    _POSTGRES_USER: str
    _POSTGRES_PASS: str
    _POSTGRES_NAME: str
    _POSTGRES_PORT: int
    _POSTGRES_HOST: str
    _DEBUG: bool

    _REDIS_HOST: str
    _REDIS_PORT: int

    _find_student_service: type[FindStudentServiceProtocol]

    __initialized: bool = False

    def __init__(self) -> None:
        if not self.__initialized:
            raise UninitializedConfig("You must call NKernelConfig.initialize, before using it")

    @classmethod
    def initialize(
        cls,
        *,
        postgres_user: str,
        postgres_pass: str,
        postgres_name: str,
        postgres_port: int,
        postgres_host: str,
        redis_host: str,
        redis_port: int,
        debug: bool,
        find_student_service: type[FindStudentServiceProtocol],
    ) -> None:
        if cls.__initialized:
            raise AlreadyInitializedConfig("You cannot initialize config more than one time.")

        cls._POSTGRES_USER = postgres_user
        cls._POSTGRES_NAME = postgres_name
        cls._POSTGRES_PASS = postgres_pass
        cls._POSTGRES_PORT = postgres_port
        cls._POSTGRES_HOST = postgres_host

        cls._REDIS_HOST = redis_host
        cls._REDIS_PORT = redis_port

        cls._DEBUG = debug

        cls._find_student_service = find_student_service

        cls.__initialized = True

    @property
    def POSTGRES_USER(self) -> str:
        return self._POSTGRES_USER

    @property
    def POSTGRES_PASS(self) -> str:
        return self._POSTGRES_PASS

    @property
    def POSTGRES_NAME(self) -> str:
        return self._POSTGRES_NAME

    @property
    def POSTGRES_PORT(self) -> int:
        return self._POSTGRES_PORT

    @property
    def POSTGRES_HOST(self) -> str:
        return self._POSTGRES_HOST

    @property
    def REDIS_HOST(self) -> str:
        return self._REDIS_HOST

    @property
    def REDIS_PORT(self) -> int:
        return self._REDIS_PORT

    @property
    def DEBUG(self) -> bool:
        return self._DEBUG

    @property
    def find_student_service(self) -> type[FindStudentServiceProtocol]:
        return self._find_student_service
