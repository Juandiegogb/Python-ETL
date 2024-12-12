-- DROP SCHEMA test1;

CREATE SCHEMA test1 AUTHORIZATION postgres;

CREATE TABLE test1.users (
	userid serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	email varchar(150) NOT NULL,
	"password" varchar(255) NOT NULL,
	address varchar(255) NULL,
	city varchar(100) NULL,
	state varchar(100) NULL,
	postalcode varchar(20) NULL,
	country varchar(100) DEFAULT 'Unknown'::character varying NULL,
	phonenumber varchar(20) NULL,
	registrationdate timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	lastlogin timestamp NULL,
	isactive bool DEFAULT true NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);