/* CREATE SCHEMAS START */

CREATE SCHEMA IF NOT EXISTS edu_info ;
CREATE SCHEMA IF NOT EXISTS attendance;
CREATE SCHEMA IF NOT EXISTS student_management;

/* CREATE SCHEMAS END */

/* CREATE TYPES START */

CREATE TYPE visit_status AS ENUM ('PRESENT', 'ABSENT');
CREATE TYPE role AS ENUM ('STUDENT', 'VICE HEADMAN', 'HEADMAN', 'ADMIN');
CREATE TYPE university_alias AS ENUM ('MIREA', 'BMSTU');

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
    group_id BIGINT REFERENCES edu_info.groups(id) ON DELETE CASCADE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role role NOT NULL,
    birthdate DATE NULL,
    attendance_noted BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS attendance.lessons (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT REFERENCES edu_info.groups(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    start_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance.attendances (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES student_management.students(id) ON DELETE CASCADE,
    lesson_id BIGINT REFERENCES attendance.lessons(id),
    status visit_status NOT NULL
);

/* CREATE TABLES END */

/* INSERT CONSTANT DATA START */

INSERT INTO edu_info.universities (name, alias, timezone) VALUES ('РТУ МИРЭА', 'MIREA', 'Europe/Moscow');
INSERT INTO edu_info.universities (name, alias, timezone) VALUES ('МГТУ им. Н.Э. Баумана', 'BMSTU', 'Europe/Moscow');

/* INSERT CONSTANT DATA END */
