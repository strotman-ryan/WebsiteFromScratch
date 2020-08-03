
#make database script
drop database Website;

create database Website;

use Website;

create table User (
	id int not null auto_increment,
	userName varchar(30) unique,
    password varchar(50),
    primary key(id),
);


create table Messages(
	id int not null auto_increment,
    message varchar(200),
    userId int not null,
    date_Time datetime not null default now(),
	foreign key (userId) references User(id),
    primary key(id)
);


insert into User(userName, password)
values("ryan", "password");

insert into User(userName, password)
values("matthew", "password");

