# Список гайдов, как что создать

## Хочу добавить новую фичу, что делать?

Для добавления нового функционала могут понадобиться такие компоненты:
- Repository - для чтения и записи данных из базы, Redis или других источников.
- Mapper - Преобразует объект (asyncpg.Record или dict), который вернет коннектор к базе в доменную сущность.
- Gateway - для взаимодействия с другим модулем.
- Contract - описывает интерфейс модуля, чтобы его потом могли использовать другие модули.
- Query - нужен для чтения из базы. Может использоваться внутри контроллера.
- Command - нужен для мутации данных. Может использовать внутри контроллера.

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

file: _src/modules/users/infrastructure/persistence/repositories/user_repository.py_
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
- Для упрощения работы используется класс UserMapper. Он должен, используя метод to_domain, трансформировать результат запроса в доменную
сущность.
