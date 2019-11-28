
create table limit_group(
    id integer primary key AUTOINCREMENT,
    title text not null,
    limit integer not null
);

create table limit_item(
    id integer primary key AUTOINCREMENT,
    foreign key (app_id) references app (id),
    foreign key (limit_group_id) references app (id)
);

create table app(
    id integer primary key AUTOINCREMENT,
    title text not null
);
