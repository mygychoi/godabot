-- Goda 2023.05.21

create table if not exists public.access_access
(
    team_id           varchar(255)                                       not null
        constraint access_access_team_id_pk
            primary key,
    team_name         varchar(255)                                       not null,
    token             varchar(255)                                       not null
        constraint access_access_token_uk
            unique,
    is_active         boolean                  default true              not null,
    organization_id   varchar(255),
    organization_name varchar(255),
    created_at        timestamp with time zone default CURRENT_TIMESTAMP not null,
    updated_at        timestamp with time zone
);

alter table public.access_access
    owner to goda;

create index if not exists access_access_created_at_ix
    on public.access_access (created_at desc);

create index if not exists access_access_is_active_ix
    on public.access_access (is_active desc);

create trigger access_access_refresh_updated_a
    before update
    on public.access_access
    for each row
execute procedure public.refresh_updated_at();
