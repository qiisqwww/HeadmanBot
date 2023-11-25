create table if not exists universities (
    id bigserial primary key,
    name varchar(255) NOT NULL UNIQUE,
    alias varchar(255) NOT NULL UNIQUE
);

create table if not exists students (
    telegram_id bigint primary key,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    birthday smallint,
    birthmonth smallint
);

create table if not exists groups (
    id bigserial primary key,
    headman_id bigint references students(telegram_id),
    university_id bigint references universities(id),
    name varchar(255) NOT NULL,
    payment_expired date NOT NULL
);

create table if not exists students_groups (
    student_id bigint references students(telegram_id),
    group_id bigint references groups(id)
);

create table if not exists lessons (
    id bigserial primary key,
    group_id bigint references groups(id) ON DELETE CASCADE,
    name varchar(255) NOT NULL,
    start_time time with time zone NOT NULL
);


create table if not exists attendances (
    student_id bigint references students(telegram_id) ON DELETE CASCADE,
    lesson_id bigint references lessons(id) ON DELETE CASCADE,
    visit_status varchar(255) NOT NULL
);
