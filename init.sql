CREATE USER boostertech WITH PASSWORD '1234';
CREATE DATABASE boostertech;
GRANT ALL PRIVILEGES ON DATABASE boostertech TO boostertech;

CREATE ROLE root LOGIN SUPERUSER PASSWORD '1234';