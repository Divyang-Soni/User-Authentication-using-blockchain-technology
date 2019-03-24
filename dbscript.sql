----------------------------- Organization details -----------------------------
CREATE TABLE IF NOT EXISTS organization_details(id serial PRIMARY KEY, name varchar(100), address_line_1 varchar(200), address_line_2 varchar(50), city varchar(50), state varchar(50), country varchar(50), zip int, phone varchar(50), headquarter varchar(50), approved int, email varchar(200), founded_date date, organization_type int, created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS organization_branch(id serial PRIMARY KEY, organization_id int NOT NULL, address_line_1 varchar(200), address_line_2 varchar(50), city varchar(50), state varchar(50), country varchar(50), zip int, phone varchar(15), created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

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

---------------------------- user details ---------------------------

CREATE TABLE IF NOT EXISTS user_basic(id serial PRIMARY KEY, given_name VARCHAR(50), last_name VARCHAR(50), dob date, email VARCHAR(50), password VARCHAR(256), user_type int, created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_profile(id serial PRIMARY KEY, user_id int NOT NULL, gender char(1), ethinicity VARCHAR(20), address_line_1 VARCHAR(200), address_line_2 VARCHAR(50), city varchar(50), state varchar(50), country_of_residence VARCHAR(50), country_of_citizenship VARCHAR(50), zip int, phone varchar(50), profile_photo VARCHAR, created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_verify(id serial PRIMARY KEY, user_id int NOT NULL, verification_id VARCHAR(50), verification_type VARCHAR(50), created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);

CREATE TABLE IF NOT EXISTS user_organization_mapping(id serial PRIMARY KEY, organization_id int NOT NULL, user_id int NOT NULL, user_role int NOT NULL, delete_flag int DEFAULT 0);

CREATE TABLE IF NOT EXISTS verification_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);
