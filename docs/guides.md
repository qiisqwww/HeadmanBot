# Список гайдов, как что создать

## Хочу добавить новую фичу, что делать?

Для добавления нового функционала могут понадобиться такие компоненты:
- Repository - для чтения и записи данных из базы, Redis или других источников.
- Mapper - Преобразует объект (asyncpg.Record или dict), который вернет коннектор к базе в доменную сущность.
- Gateway - для взаимодействия с другим модулем или внешними API.
- Contract - описывает интерфейс модуля, чтобы его потом могли использовать другие модули.
- Query - нужен для чтения из базы. Может использоваться внутри контроллера.
- Command - нужен для мутации данных. Может использовать внутри контроллера.

А также потребуется сконфигурировать DI контейнер.

## Как создать Repository 

Чтобы сделать репозиторий, нам понадобиться описать его интерфейс и реализацию.
Допустим, наш текущий модуль называется *users*, и мы хотим сделать *UserRepository* для работы с таблицей users. 

Правило наименования - интерфейсы НЕ содержат заглавную букву I в начале. Нет никаких *IUserRepository*. А
вот уже реализация содержит суффикс *Impl*, и получиться - *UserRepositoryImpl*.

Создадим интерфейс репозитория:

file: _src/modules/users/application/repositories/user_repository.py_
```py 
class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def create(self, name: str, surname: str, age: int) -> User:
        ...
```

В данном случае User - это сущность из слоя domain. ОНа может быть описана в файле _src/modules/users/domain/models/user.py_

А теперь напишем реализацию репозитория:

file: _src/modules/users/infrastructure/repositories/user_repository.py_
```py
@final
class UserRepositoryImpl(PostgresRepositoryImpl, UserRepository):
    _mapper: UserMapper = UserMapper()

    async def find_by_id(self, user_id: int) -> User | None:
        query = "SELECT id,name,surname,age FROM users.users"

        record = await self._con.fetchrow(query, student_id)

        if record is None:
            return None

        return self._mapper.to_domain(record)

    async def create(self, name: str, surname: str, age: int) -> User:
        query = """INSERT INTO users.users (name, surname, age)
                   VALUES ($1, $2, $3) RETURNING id"""

        user_id = await self._con.fetchval(query, name, surname, age)

        return User(
            id=user_id,
            name=name,
            surname=surname,
            age=age,
        )
```
Важные детали:
- Реализация репозитория должна быть *final*.
- Мы должны еще отнаследоваться от класса *PostgresRepositoryImpl* или *RedisRepositoryImpl*, в которых уже прописана логика инъекции
подключения к базе данных
- Объект подключения лежит в аттрибуте *self._con*.
- Репозиторий всегда возвращает валидную доменную сущность или None. В крайнем случае bool для метод exists.
- Для упрощения работы используется класс UserMapper. Он должен, используя метод to_domain, трансформировать результат 
запроса в доменную сущность.

## DataMapper

Как уже было видно, это репозиторий используей некий _UserMapper_. Что же должен делать DataMapper?
Он может преобразовать словарь в доменную сущность и обратно. Также может преобразовать некий DTO в словарь, который
потом можно будет положить в redis и наоборот.

file: _src/modules/users/infrastructure/mappers/user_mapper.py_

```py 
@final
class UserMapper:
    def to_domain(self, data: Mapping) -> User:
        return User(
            id=data['id'],
            name=data['name'],
            surname=data['surname'],
            age=data['age'],
        )
```

Важные детали:
- Класс Mapper должен быть final.
- В данном случае мы зависимость в виде маппера хардкодим прямо в репозиторий.

## Репозиторий готов, а что дальше?

Дальше нам нужно описать Query и комманд, которые уже можно будет использовать в контроллерах.

## Как написать Query и Command

Query может только читать данные. Его задача - это максимально эффективно достать данные для отображения их пользователю.

file: _src/modules/users/application/queries/find_user_query.py_
```py
@final
class FindUserQuery(UseCase):
    _repository: UserRepository

    @inject
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: int) -> User | None:
        return await self._repository.find_by_id(user_id)
```
Command уже может мутировать данные, а также отдавать пользователю какой-то результат.

file: _src/modules/users/application/commands/create_user_command.py_
```py
@final
class CreateUserCommand(UseCase):
    _repository: UserRepository

    @inject
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, name: str, surname: str, age: int) -> User:
        return await self._repository.create(name, surname, age)
```
Важные детали:
- Классы Command и Query должны быть final.
- Эти классы наследуются от UseCase. Иначе **РАБОТАТЬ НИЧЕГО НЕ БУДЕТ**.
- Над конструктором должен быть прописан декоратор _@inject_.
- Все зависимости в виде репозиториев и gateways описываются в конструкторе через их интерфейсы.

Но тогда возникают вопросы: как использовать эти useCases в контроллерах и что такое _@inject_? Тут мы плавно подходим к настройке DI 
контейнера.


## DI контейнер

Как DI контейнер используется бибилиотека injector.

Что из себя представляет DI контейнер? DI контейнер - это некий инструмент, который будет для нас собирать useCases и все их зависимости.
А потом мы сможешь просто написать 
```py 
create_user_command = container.get(CreateUserCommand)
```

В контейнер просто передается класс нужной нам комманды или запроса, и контейнер соберет нам валидный объект комманды.
Но как он понимает, что нужно для сборки _CreateUserCommand_? Для этого мы и должны описать процесс сборки.

Нужно описать зависимости для объектов, который будет собирать DI контейнер. Для этого и нужен декоратор _@inject_. Он пишется
для конструктора. Таким же образом репозитории требует объект Connection. Для инъекции в них этого объекта декоратор _@inject_ описывается
в базовых классах PostgresRepositoryImpl и RedisRepositoryImpl.

Также нужно описать связь между интерфейсом репозитория и его реализацией. Для этого нам понадобиться объект binder.

file: _src/modules/users/infrastructure/container.py_
```py
from injector import Binder, singleton

def assemble_user_module(binder: Binder) -> None:
    binder.bind(UserRepository, UserRepositoryImpl, singleton) # Момент связывания интерфейса и его реализации.
```

Через binder мы описываем связь между интерфейсом и реализацией DI контейнеру. _singleton_ - это константа из библиотеки injector.
Используя ее, injector создаст репозиторий только ОДИН раз. И одни и тот же репозиторий может использовать для нескольких useCases.

Если функция *assemble_<module_name>_module* уже была, то просто дописываем в конце binder.bind.
Если нет, то нам нужно подключить сборку данного модуля в общий контейнер. 

file: _src/modules/common/infrastructure/container.py_
```py 
from src.modules.usesr.infrastructure.container import assemble_users_module

...

def assemble_modules(binder: Binder) -> None:
    assemble_common_dependencies(binder)

    ...

    assemble_users_module(binder) # Дописываем в конец этой функции эту строчку и все, зависимости
    # из модуля users теперь доступны в общем контейнере.

...
```

Настройка DI завершена, нам осталось только использовать эти два useCases в контроллерах. Для этого просто в сигнатуре функции контроллера
прописываем их как параметры с соотвествующими им типами.

## Как создавать и использовать контроллеры

```py
from aiogram.types import Message

from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.common.router import RootRouter, Router

from src.modules.users.application.commands import CreateUserCommand


__all__ = [
    "include_start_command_router",
]

start_command_router = Router()

@start_command_router.message(CommandFilter(TelegramCommand.START))
async def start_command(
        message: Message,
        create_user_command: CreateUserCommand, # Прописываем CreateUserCommand как зависимость для этого контроллера
) -> None:
    name, surname, age = message.text.split()
    await create_user_command.execute(name, surname, age)


def include_start_command_router(root_router: RootRouter) -> None:
    root_router.include_router(start_command_router)
```

Есть два типа роутеров:
- RootRouter - он один на всего бота. Он подключается в dispatcher. в нем можно настроить throttling.
- Router - один для одной комманды/callback. В нем настривается инъекция пользователя и права доступа для этого роутера.

Функции include_router можно группировать как угодно, по модулям и т. д. Главное потом вставить эту функцию в 

file: _src/bot/modules/\_\_init\_\_.py_
```py 
from src.bot.common.router import RootRouter

def include_all_routers(root_router: RootRouter) -> None:
    include_start_command_router(root_router)
```

В остальном можно делать уже по аналогии с написаным кодом.

## Взаимодействие между модулями 

А что если мы хотим как-то взаимодействовать с другим модулем? Нам нужно будет реализовать contract другого модуля и gateway, который
будет уметь взаимодействовать с этим контрактом.

file: _src/modules/analitics/contract.py_
```py
class AnaliticsModuleContract(ABC):
    @abstractmethod
    async def safe_user_for_analitics(self, user_id: int, name: str, surname: str) -> None:
        ...
```

Ниже будет находиться реализация контракта. Там может быть что угодно.

file: _src/modules/analitics/infrastructure/contract.py_

file: _src/modules/users/applications/gateways/analitics_module_gateway.py_
```py
class AnaliticsModuleGateway(ABC):
    _contract: AnaliticsModuleContract

    @abstractmethod
    async def safe_user_for_analitics(self, user: User) -> None:
        ...
```

И реализация:

```py
@final
class AnaliticsModuleGatewayImpl(AnaliticsModuleGateway):
    _contract: AnaliticsModuleContract

    @inject
    def __init__(self, contract: AnaliticsModuleContract) -> None:
        self._contract = contract

    async def safe_user_for_analitics(self, user: User) -> None:
        await self._contract.safe_user_for_analitics(user.id, user.name. user.surname)
```
Этот gateway уже можно использовать в users/application

file: _src/modules/users/application/commands/create_user_command.py_
```py 
@final
class CreateUserCommand(UseCase):
    _repository: UserRepository
    _gateway: AnaliticsModuleGateway

    @inject
    def __init__(self, repository: UserRepository, gateway: AnaliticsModuleGateway) -> None:
        self._repository = repository

    async def execute(self, name: str, surname: str, age: int) -> User:
        user = await self._repository.create(name, surname, age)
        await self._gateway.safe_user_for_analitics(user)
        return user
```

Таким образом мы используем код из другово модуля.

Важные детали:
- Реализиация contract и gateway пишется по аналогии с репозиториями: классы должны быть final c декоратором @inject 
- Не забудь описать в DI контейнере связь между интерфейсов контракта и его реализацией, тоже и для gateway.
