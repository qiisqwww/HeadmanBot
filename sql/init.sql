/* CREATE TYPES START */

CREATE TYPE visit_status AS ENUM ('present', 'absent');
CREATE TYPE role AS ENUM ('student', 'vice headman', 'headman', 'admin');
CREATE TYPE university_alias AS ENUM ('MIREA', 'BMSTU');

/* CREATE TYPES END */

/* CREATE TABLES START */

create table if not exists universities (
    id bigserial primary key,
    name varchar(255) NOT NULL,
    alias university_alias NOT NULL UNIQUE
);

create table if not exists groups (
    id bigserial primary key,
    university_id bigint references universities(id) ON DELETE CASCADE,
    name varchar(255) NOT NULL
);

create table if not exists students (
    telegram_id bigint primary key,
    group_id bigint references groups(id) ON DELETE CASCADE,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    role role NOT NULL,
    birthdate date NULL,
    is_checked_in_today boolean NOT NULL
);


create table if not exists lessons (
    id bigserial primary key,
    group_id bigint references groups(id) ON DELETE CASCADE,
    name varchar(255) NOT NULL,
    start_time time with time zone NOT NULL
);

create table if not exists attendances (
    id bigserial primary key,
    student_id bigint references students(telegram_id) ON DELETE CASCADE,
    lesson_id bigint references lessons(id),
    status visit_status NOT NULL
);

/* CREATE TABLES END */
