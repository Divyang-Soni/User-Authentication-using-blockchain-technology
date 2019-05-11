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
INSERT INTO record_type (type) values ('criminal');
INSERT INTO record_type (type) values ('residential');

---------------------------- user details ---------------------------

CREATE TABLE IF NOT EXISTS user_basic(id serial PRIMARY KEY, given_name VARCHAR(50), last_name VARCHAR(50), dob date, email VARCHAR(50), password VARCHAR(256), user_type int, created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_profile(id serial PRIMARY KEY, user_id int NOT NULL, gender char(1), ethnicity VARCHAR(20), address_line_1 VARCHAR(200), address_line_2 VARCHAR(50), city varchar(50), state varchar(50), country_of_residence VARCHAR(50), country_of_citizenship VARCHAR(50), zip int, phone varchar(50), profile_photo VARCHAR, created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_verify(id serial PRIMARY KEY, user_id int NOT NULL, verification_id VARCHAR(50), verification_type VARCHAR(50), created_date date, created_by int, modified_date date, modified_by int, delete_flag int DEFAULT 0, deleted_by int);

CREATE TABLE IF NOT EXISTS user_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);
INSERT INTO user_type (type) values ('admin');
INSERT INTO user_type (type) values ('org_admin');
INSERT INTO user_type (type) values ('org_user');
INSERT INTO user_type (type) values ('user');

CREATE TABLE IF NOT EXISTS user_organization_mapping(id serial PRIMARY KEY, organization_id int NOT NULL, user_id int NOT NULL, user_role int NOT NULL, delete_flag int DEFAULT 0);

CREATE TABLE IF NOT EXISTS verification_type(id serial PRIMARY KEY, type VARCHAR(50) UNIQUE, delete_flag int DEFAULT 0);

----------------------------- block data -----------------------------


CREATE TABLE IF NOT EXISTS data_request(id serial PRIMARY KEY , from_id int NOT NULL, for_id int NOT NULL, data_category int NOT NULL, requested_datetime date NOT NULL, status int default 0, response_time date, review_date date)

update data_request set status = 0 where id > 0;
