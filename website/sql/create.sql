create table user
(
    uid      int auto_increment
        primary key,
    name     varchar(50)              null,
    email    varchar(100)             not null,
    type     enum ('admin', 'normal') not null,
    password varchar(50)              not null
)
    comment 'User Info';

create table record
(
    rid   int auto_increment comment 'Unique identification of a record'
        primary key,
    uid   int                                not null,
    emoji int                                not null comment 'emoji ID',
    time  datetime default CURRENT_TIMESTAMP not null,
    constraint record_user_uid_fk
        foreign key (uid) references user (uid),
    constraint emoji_constraint
        check ((`emoji` >= 0) and (`emoji` < 6))
)
    comment 'Record of emojis sent by users';

