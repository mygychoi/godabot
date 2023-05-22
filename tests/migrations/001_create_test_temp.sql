-- Goda 2023-05-20 16:02

create table public.test_temp
(
    id   integer primary key not null default nextval('test_temp_id_seq'::regclass),
    name character varying(256)
);
