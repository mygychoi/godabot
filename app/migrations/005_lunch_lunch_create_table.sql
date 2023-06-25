-- Goda 2023.06.25

create table lunch_lunch
(
    id serial not null constraint lunch_lunch_id_pk primary key,
    title varchar(255) not null,
    preference text not null,
    recommendation text not null,
    created_at timestamptz default current_timestamp not null,
    updated_at timestamptz,

    roulette_id integer not null
        constraint lunch_lunch_roulette_id_fk
            references lunch_roulette
            on delete cascade
);

create index lunch_lunch_created_at_ix
    on lunch_lunch (created_at desc);

create index lunch_lunch_roulette_id_ix
    on lunch_lunch (roulette_id);

create trigger lunch_lunch_refresh_updated_at
    before update
    on lunch_lunch
    for each row
execute procedure refresh_updated_at();
