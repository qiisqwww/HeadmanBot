create table if not exists groups (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE,
);

create table if not exists lessons (
    id bigserial primary key,
    discipline varchar(255) NOT NULL,
    start_time time with timezone NOT NULL,
);

create table if not exists universities (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE,
);

create table if not exists users (
    telegram_id bigint primary key,
    group_id bigint references groups(id),
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    telegram_name varchar(255) NULL,
    is_headman boolean NOT NULL DEFAULT false,
);

create table if not exists schedule (
    group_id bigint references groups(id),
    lesson_id bigint references lessons(id),
    lesson_num smallint NOT NULL,
    day_number smallint NOT NULL,
);

create table if not exists attendance (
    user_id bigint references users(telegram_id),
    group_id bigint references groups(id),
    visit_status varchar(255) NOT NULL,
);
