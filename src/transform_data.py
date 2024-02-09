import sqlite3
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import date

from injector import Injector

from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.student_management.application.commands.register_student_command import RegisterStudentCommand
from src.modules.student_management.domain.enums.role import Role

MIREA_ID = 1


@dataclass
class User:
    telegram_id: int
    first_name: str
    last_name: str
    birthdate: date | None
    role: Role
    group_name: str
    university_alias: UniversityAlias


def get_users(cursor: sqlite3.Cursor) -> list[User]:
    query = "SELECT telegram_id,user_name,name_surname,study_group,is_headmen FROM students"
    rows = cursor.execute(query).fetchall()

    users: list[User] = []

    for row in rows:
        telegram_id = int(row[0])
        telegram_name = row[1] if row[1] != "" else None

        if telegram_name == "nitrowp":
            _, name, surname = row[2].split()
        elif telegram_name == "kolyan677":
            surname, _, name = row[2].split()
        elif telegram_name == "Yyandhi":
            surname, name, *_ = row[2].split()

        else:
            surname, name = row[2].split()

        group_name = row[3]
        is_headman = bool(row[4])

        users.append(
            User(
                telegram_id=telegram_id,
                first_name=name,
                last_name=surname,
                birthdate=None,
                role = Role.HEADMAN if is_headman else Role.STUDENT,
                group_name=group_name,
                university_alias=UniversityAlias.MIREA,
            ),
        )

    return users


async def transform(project_container: Callable[[], AbstractAsyncContextManager[Injector]]) -> None:
    conn = sqlite3.connect("./bot.db")
    cursor = conn.cursor()
    users = get_users(cursor)
    cursor.close()

    async with project_container() as container:
        command = container.get(RegisterStudentCommand)
        for user in users:
            print(user)
            await command.execute(user.telegram_id, user)
