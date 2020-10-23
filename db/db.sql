create table user(uid varchar(6) primary key,email text not null, pswd varchar(30))engine=Innodb;

create table therapist (fname text not null, lname text not null, gender varchar(1) not null,qualification text not null,years_of_exp float not null,phone_number varchar(10) not null,uid varchar(6),constraint foreign key(uid)  references user(uid))engine=Innodb;

create table client (fname text not null, lname text not null, mname text not null, gender varchar(1) not null,security_question text not null,answer text not null,phone_number varchar(10) not null, dob date, uid varchar(6),constraint foreign key(uid) references user(uid))engine=Innodb;

create table test(tid varchar(1) primary key, time_limit int)engine=Innodb;

create table psychotest(qid varchar(2) primary key,question_description text ,tid varchar(1),constraint foreign key(tid) references test(tid))engine=Innodb;

create table iqtest(qid varchar(2) primary key, question_description text,  option1 text, option2 text, option3 text, option4 text,correct_answer text, tid varchar(1),constraint foreign key(tid) references  test(tid))engine=Innodb;

create table client_test(uid varchar(6),tid varchar(1),score varchar(2),constraint foreign key(uid) references client(uid),constraint foreign key(tid) references test(tid))engine=Innodb;

create table message(message_id varchar(6) primary key,uid varchar(6),msg_desc text,reciever varchar(6),datetime DATETIME,constraint foreign key(uid) references user(uid))engine=Innodb; 
