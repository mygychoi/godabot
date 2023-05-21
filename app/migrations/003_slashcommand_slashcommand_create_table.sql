-- Goda 2023.05.21

create table slashcommand_slashcommand
(
    id         serial       not null
        constraint slashcommand_slashcommand_id_pk
            primary key,
    team_id    varchar(255) not null,
    team_name  varchar(255) not null,
    command    varchar(255) not null,
    created_at timestamptz default current_timestamp
);

create index slashcommand_slashcommand_created_at_ix
    on slashcommand_slashcommand (created_at desc);
