create table if not exists groups (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE
);

create table if not exists lessons (
    id bigserial primary key,
    group_id bigint references groups(id),
    discipline varchar(255) NOT NULL,
    start_time time with time zone NOT NULL,
    weekday smallint NOT NULL
);

create table if not exists universities (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE
);

create table if not exists students (
    telegram_id bigint primary key,
    group_id bigint references groups(id),
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    telegram_name varchar(255) NULL,
    is_headman boolean NOT NULL DEFAULT false
);


create table if not exists attendance (
    student_id bigint references students(telegram_id),
    lesson_id bigint references lessons(id),
    visit_status varchar(255) NOT NULL
);
