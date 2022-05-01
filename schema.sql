DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    email varchar(200),
    password_hash varchar(100)
);

CREATE TABLE movies (
    id serial PRIMARY KEY,
    imdb_id varchar(15) NOT NULL,
    whose_pick integer,
    FOREIGN KEY(whose_pick)
      REFERENCES users(id),
    title varchar(50),
    date_watched date,
    country varchar(20),
    release_year integer,
    img_src varchar(300),
    synopsis varchar(3000)
);