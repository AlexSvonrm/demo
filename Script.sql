CREATE TABLE IF NOT EXISTS Genre (
	ID_Genre SERIAL PRIMARY KEY,
	Name_Genre VARCHAR(80) not null);

CREATE TABLE IF NOT EXISTS Singer (
	ID_Singer SERIAL primary key,
	ID_Genre INTEGER not null references Genre(ID_Genre),
	Name_Singer VARCHAR(80) not null);

CREATE TABLE IF NOT EXISTS Album (
	ID_Album SERIAL PRIMARY KEY,
	ID_Singer INTEGER NOT NULL REFERENCES Singer(ID_Singer),
	Name_Album VARCHAR(80) NOT NULL,
	Yearset INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS Track (
	ID_Track SERIAL PRIMARY KEY,
	ID_Album INTEGER NOT NULL REFERENCES Album(ID_Album),
	Name_Track VARCHAR(80) NOT NULL,
	Duration FLOAT);

