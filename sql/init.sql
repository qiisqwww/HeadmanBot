/* CREATE TABLES START */

create table if not exists universities (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE,
    alias varchar(255) NOT NULL UNIQUE
);

create table if not exists groups (
    id bigserial primary key,
    university_id bigint NOT NULL,
    name varchar(255) NOT NULL
);

create table if not exists students (
    telegram_id bigint primary key,
    group_id bigint references groups(id),
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    role varchar(255) NOT NULL,
    birthdate date NULL
);


create table if not exists lessons (
    id bigserial primary key,
    group_id bigint references groups(id),
    name varchar(255) NOT NULL,
    start_time time with time zone NOT NULL
);

create table if not exists attendances (
    student_id bigint references students(telegram_id),
    lesson_id bigint references lessons(id),
    visit_status varchar(255) NOT NULL
);

/* CREATE TABLES END */
