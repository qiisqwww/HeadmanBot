from loguru import logger

from src.modules.edu_info.application.commands import InsertUniversitiesCommand
from src.modules.edu_info.infrastructure.repositories import UniversityRepositoryImpl

from .postgres import get_postgres_pool

__all__ = [
    "init_database",
]

INIT_DATABASE_SQL = """
/* CREATE SCHEMAS START */

CREATE SCHEMA IF NOT EXISTS edu_info ;
CREATE SCHEMA IF NOT EXISTS attendance;
CREATE SCHEMA IF NOT EXISTS student_management;

/* CREATE SCHEMAS END */

/* CREATE TYPES START */

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'visit_status') THEN
        CREATE TYPE visit_status AS ENUM ('present', 'absent');
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
        CREATE TYPE role AS ENUM ('student', 'vice headman', 'headman', 'admin');
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'university_alias') THEN
        CREATE TYPE university_alias AS ENUM ('MIREA', 'BMSTU');
    END IF;
END
$$;

/* CREATE TYPES END */

/* CREATE TABLES START */

CREATE TABLE IF NOT EXISTS edu_info.universities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alias university_alias NOT NULL UNIQUE,
    timezone varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS edu_info.groups (
    id BIGSERIAL PRIMARY KEY,
    university_id BIGINT REFERENCES edu_info.universities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS student_management.students (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    group_id BIGINT,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    role role NOT NULL,
    birthdate DATE NULL,
    is_checked_in_today BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS attendance.lessons (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT,
    name VARCHAR(255) NOT NULL,
    start_time TIME WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance.attendances (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT,
    lesson_id BIGINT REFERENCES attendance.lessons(id),
    status visit_status NOT NULL
);

/* CREATE TABLES END */
"""

async def init_database() -> None:
    logger.info("Start initalizing database.")
    pool = await get_postgres_pool()

    async with pool.acquire() as con:
        await con.execute(INIT_DATABASE_SQL)
        insert_universities_command = InsertUniversitiesCommand(UniversityRepositoryImpl(con))
        await insert_universities_command.execute()
    logger.info("Finish initalizing database.")
