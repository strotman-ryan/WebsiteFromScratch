/*
#make database script
drop database Website;

CREATE DATABASE Website;

create table User (
	id int not null AUTO_INCREMENT,
	userName varchar(30),
    password varchar(50),
    primary key(id)
);


create table Messages(
	id int,
    message varchar(20),
	foreign key (id) references User(id) 
);
*/