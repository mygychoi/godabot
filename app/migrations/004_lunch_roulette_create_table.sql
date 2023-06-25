-- Goda 2023.06.25

create table lunch_roulette
(
    id serial not null constraint lunch_roulette_id_pk primary key,
    channel_id varchar(255) not null,
    title text not null,
    status varchar(9) default 'scheduled' not null,
    spin_at timestamptz not null,
    created_at timestamptz default current_timestamp not null,
    updated_at timestamptz
);

create index lunch_roulette_created_at_ix
    on lunch_roulette (created_at desc);

create index lunch_roulette_channel_id_ix
    on lunch_roulette (channel_id);

create index lunch_roulette_status_ix
    on lunch_roulette (status);

create unique index lunch_roulette_channel_id_status_uix
    on lunch_roulette (channel_id, status)
    where status = 'scheduled';

create trigger lunch_roulette_refresh_updated_at
    before update
    on lunch_roulette
    for each row
execute procedure refresh_updated_at();
