/*This file contains psql script for db creation and table creation*/
sudo -u postgres psql //starts psql with postgres as superuser for first time
createuser --interactive //creates new user
(add new user's name & his role) (for eg raj & assign superuser role)
createdb UABT; //creates new database
exit
sudo -u raj psql //connects postgres with this user
\c UABT //connects to this db

CREATE TABLE company_details(cid serial PRIMARY KEY, pid int, name varchar(100), address varchar(200), city varchar(50), state varchar(50), country varchar(50), zip int, phone varchar(50), headquarter varchar(50), founded_date date, organization_type varchar(50), size int, created_date date, created_by int, modified_date date, modified_by int);

