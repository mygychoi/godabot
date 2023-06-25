-- Goda 2023.06.25

create table lunch_attendance
(
    id serial not null constraint lunch_attendance_id_pk primary key,
    user_id varchar(255) not null,
    user_name varchar(255) not null,
    preference text not null,
    created_at timestamptz default current_timestamp not null,
    updated_at timestamptz,

    roulette_id integer not null
        constraint lunch_attendance_roulette_id_fk
            references lunch_roulette
            on delete cascade,
    lunch_id integer
        constraint lunch_attendance_lunch_id_fk
            references lunch_lunch
            on delete cascade,

    constraint lunch_attendance_user_id_roulette_id_u
    unique (user_id, roulette_id),
    constraint lunch_attendance_user_id_lunch_id_u
    unique (user_id, lunch_id)
);

create index lunch_attendance_created_at_ix
    on lunch_attendance (created_at desc);

create index lunch_attendance_user_id_ix
    on lunch_attendance (user_id);

create index lunch_attendance_roulette_id_ix
    on lunch_attendance (roulette_id);

create index lunch_attendance_lunch_id_ix
    on lunch_attendance (lunch_id);

create trigger lunch_attendance_refresh_updated_at
    before update
    on lunch_attendance
    for each row
execute procedure refresh_updated_at();
