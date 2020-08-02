SELECT * FROM Website.Messages;


select Message.* 
from Messages
inner join User on User.id = Messages.userId
where Messages.userId = 1;

#this is used to add messages
insert into Messages (message, userId)
values("this is matthew", (select id from User where userName = 'matthew'));