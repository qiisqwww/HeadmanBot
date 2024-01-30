# Список гайдов, как что создать

## Хочу добавить новую фичу, что делать?

Для добавления нового функционала могут понадобиться такие компоненты:
- Repository - для чтения данных из базы или Redis
- Mapper - Преобразует Record объект, который вернет коннектор к базе в domain model
- Query - нужен для чтения из базы. Может использоваться внутри контроллера.
- Command - нужен для мутации данных. Может использовать внутри контроллера.
- Gateway - для взаимодействия с другим модулем.

## Как создать Repository 

Чтобы сделать репозиторий нам понадобиться сделать его интерфейс и реализацию.
Допустим наш текущий модуль называется users и мы хотим сделать UserRepository для работы с таблице users. 

Первое правило: интерфейсы репозиториев НЕ содержат заглавную букву I в начале. Нет никаких IUserRepository. А
вот уже реализация содераржит суффикс Impl и получиться - UserRepositoryImpl.

Создадим интерфейс репозитория:

file: src/modules/users/application/repositories/user_repository.py
```py 
class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def create(self, name: str, surname: str, age: int) -> User:
        ...
```

В данном случае User - это сущность из слоя domain. Может лежать в файле src/modules/users/domain/models/user.py

А теперь напишем реализацию репозитория:

file: src/modules/users/infrastructure/persistence/repositories/user_repository.py
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
- Реализация репозитория должна быть final
- Мы должны еще отнаследоваться от класса PostgresRepositoryImpl или RedisRepositoryImpl в которых уже прописана логика инъекции
подключения к базе данных
- Объект подключения лежит в аттрибуте self._con 
- Репозиторий всегда возвращает валидную доменную сущность или None. В крайнем случае bool для метод exists
- Для упрощения работы используется класс UserMapper. Он должен, используя метод to_domain перегонять результат запроса в доменную
сущность
