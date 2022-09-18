drop table if exists todos;
create table todos
( id            text not null primary key
, content       text not null
, stat          smallint not null
, create_time   time not null
, resolve_time
);

insert into todos values ('00000000-0000-0000-0000-000000000001', 'My first thing todo', 0, current_time, null);
insert into todos values ('00000000-0000-0000-0000-000000000002', 'Another dreadful chore', 0, current_time, null);
insert into todos values ('00000000-0000-0000-0000-000000000003', 'God it doesn''t stop', 0, current_time, null);