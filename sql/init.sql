/* CREATE SCHEMAS START */

CREATE SCHEMA IF NOT EXISTS students;
CREATE SCHEMA IF NOT EXISTS birthdates;
CREATE SCHEMA IF NOT EXISTS groups;
CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS universities;
CREATE SCHEMA IF NOT EXISTS attendances;

/* CREATE SCHEMAS END */


/* CREATE TABLES START */

create table if not exists universities.universities (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE,
    alias varchar(255) NOT NULL UNIQUE
);

create table if not exists students.students (
    telegram_id bigint primary key,
    group_id bigint NOT NULL,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    role varchar(255) NOT NULL
);

create table if not exists birthdates.birthdates (
    student_id bigint NOT NULL,
    birthdate date NULL
);

create table if not exists groups.groups (
    id bigserial primary key,
    university_id bigint NOT NULL,
    name varchar(255) NOT NULL
);

create table if not exists attendances.lessons (
    id bigserial primary key,
    group_id bigint NOT NULL,
    name varchar(255) NOT NULL,
    start_time time with time zone NOT NULL
);

create table if not exists attendances.attendances (
    student_id bigint NOT NULL,
    lesson_id bigint NOT NULL,
    visit_status varchar(255) NOT NULL
);

/* CREATE TABLES END */
