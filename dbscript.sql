----------------------------- Organization details -----------------------------
CREATE TABLE IF NOT EXISTS organization_details(id serial PRIMARY KEY, name varchar(100), address_line_1 varchar(200), city varchar(50), state varchar(50), country varchar(50), zip int, phone varchar(50), headquarter varchar(50), founded_date date, organization_type int, created_date date, created_by int, modified_date date, modified_by int, delete_flag int, deleted_by int);

CREATE TABLE IF NOT EXISTS organization_branch(id serial PRIMARY KEY, organization_id int NOT NULL, address_line_1 varchar(200), city varchar(50), state varchar(50), country varchar(50), zip int, phone varchar(15), created_date date, created_by int, modified_date date, modified_by int, delete_flag int, deleted_by int);

----------------------------- organization types ----------------------------

CREATE TABLE IF NOT EXISTS organization_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);

INSERT INTO organization_type (type) values ('educational');
INSERT INTO organization_type (type) values ('medical');
INSERT INTO organization_type (type) values ('it');
INSERT INTO organization_type (type) values ('government');

----------------------------- record types ----------------------------

CREATE TABLE IF NOT EXISTS record_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);

INSERT INTO record_type (type) values ('educational');
INSERT INTO record_type (type) values ('medical');
INSERT INTO record_type (type) values ('employment');
INSERT INTO record_type (type) values ('driving');

