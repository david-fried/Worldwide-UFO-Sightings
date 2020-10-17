DROP TABLE IF EXISTS ufo_data1_2_2014;

CREATE TABLE ufo_data1_2_2014(
		datetime VARCHAR,
		city VARCHAR,
		state VARCHAR,
		country VARCHAR,
		shape VARCHAR,
		"duration (seconds)" VARCHAR,
		"duration (hours/min)" VARCHAR,
		comments VARCHAR,
		"date posted" VARCHAR,
		latitude VARCHAR,
		longitude VARCHAR,
		year FLOAT,
		month FLOAT,
	    PRIMARY KEY (state));
	
DROP TABLE IF EXISTS state_stats;

CREATE TABLE state_stats(
	"State Name" VARCHAR,
	"Drug Deaths" INT,
	"State Abbreviation" VARCHAR,
	Sightings INT,
	AvgSightingDuration FLOAT,
	"State Codes" VARCHAR,
	"State Census Area" FLOAT,
 PRIMARY KEY ("State Abbreviation"));

DROP TABLE IF EXISTS ufo_data;

CREATE TABLE ufo_data(
		datetime VARCHAR NOT NULL,
		city VARCHAR NOT NULL,
		state VARCHAR NOT NULL,
		country VARCHAR  NOT NULL,
		shape VARCHAR NOT NULL,
		"duration (seconds)" VARCHAR NOT NULL,
		"duration (hours/min)" VARCHAR NOT NULL,
		comments VARCHAR NOT NULL,
		"date posted" VARCHAR NOT NULL,
		latitude FLOAT NOT NULL,
		longitude FLOAT NOT NULL,
	    PRIMARY KEY (state));

select * from state_stats;
