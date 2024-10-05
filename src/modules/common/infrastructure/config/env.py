from os import getenv

__all__ = [
    "UndefinedEnvError",
    "Env",
    "EnvList",
]

class UndefinedEnvError(Exception):
    """Raise when cannot read env variable and getenv return None."""

    def __init__(self, env_name: str) -> None:
        msg = f'Env name="{env_name}"'
        super().__init__(msg)


def Env[T](env_name: str, variable_type: type[T]) -> T:
    env = getenv(env_name, None)


    if env is None:
        raise UndefinedEnvError(env_name)

    if issubclass(variable_type, bool):
        return env.lower() in ("1", "true", "t")

    return variable_type(env)


def EnvList[T](env_name: str, list_item_type: type[T]) -> list[T]:
    env = getenv(env_name, None)

    if env is None:
        raise UndefinedEnvError(env_name)

    return map(list_item_type, env.split())
