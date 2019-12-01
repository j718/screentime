
drop table if exists limit_group;
drop table if exists limit_item;
drop table if exists app;

create table limit_group(
    id integer primary key AUTOINCREMENT,
    title text not null,
    time_limit integer not null
);

create table limit_item(
    id integer primary key AUTOINCREMENT,
    app_id integer not null,
    limit_group_id integer not null,
    foreign key (app_id) references app (id),
    foreign key (limit_group_id) references limit_group (id),
    UNIQUE (app_id, limit_group_id)
);

create table app(
    id integer primary key AUTOINCREMENT,
    title text not null,
    UNIQUE(title)
);

CREATE TABLE limit_increase(
    id integer primary key AUTOINCREMENT,
    day date,
    time_limit integer not null,
    limit_group_id integer not null,
    foreign key (limit_group_id) references limit_group (id)
);
