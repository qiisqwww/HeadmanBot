/* CREATE TYPES START */

CREATE TYPE visit_status AS ENUM ('PRESENT', 'ABSENT');
CREATE TYPE role AS ENUM ('IS REGISTERED', 'STUDENT', 'VICE HEADMAN', 'HEADMAN', 'ADMIN');
CREATE TYPE university_alias AS ENUM ('MIREA', 'BMSTU', 'NSTU', 'STU');

/* CREATE TYPES END */

/* CREATE TABLES START */

CREATE TABLE IF NOT EXISTS universities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alias university_alias NOT NULL,
    timezone VARCHAR(255) NOT NULL,
    archived BOOL NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX unique_university_alias ON universities(alias) WHERE NOT archived;

CREATE TABLE IF NOT EXISTS groups (
    id BIGSERIAL PRIMARY KEY,
    university_id BIGINT REFERENCES universities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    archived BOOL NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    group_id BIGINT REFERENCES groups(id),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) DEFAULT NULL,
    role role NOT NULL,
    birthdate DATE NULL,
    attendance_noted BOOL NOT NULL,
    archived BOOL NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX unique_student_telegram_id ON students(telegram_id) WHERE NOT archived;

CREATE TABLE IF NOT EXISTS lessons (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT REFERENCES groups(id),
    name VARCHAR(255) NOT NULL,
    start_time TIME NOT NULL,
    archived BOOL NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS attendances (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES students(id),
    lesson_id BIGINT REFERENCES lessons(id),
    date DATE NOT NULL,
    status visit_status NOT NULL,
    archived BOOL NOT NULL DEFAULT FALSE
);

/* CREATE TABLES END */

/* INSERT CONSTANT DATA START */

INSERT INTO universities (name, alias, timezone) VALUES ('РТУ МИРЭА', 'MIREA', 'Europe/Moscow');
INSERT INTO universities (name, alias, timezone) VALUES ('МГТУ им. Н.Э. Баумана', 'BMSTU', 'Europe/Moscow');
INSERT INTO universities (name, alias, timezone) VALUES ('НГТУ', 'NSTU', 'Asia/Novosibirsk');
INSERT INTO universities (name, alias, timezone) VALUES ('СГУПС', 'STU', 'Asia/Novosibirsk');

/* INSERT CONSTANT DATA END */
