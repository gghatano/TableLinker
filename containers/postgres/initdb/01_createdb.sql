CREATE USER tablelinker WITH PASSWORD 'tablelinker';
ALTER ROLE tablelinker CREATEDB;
ALTER ROLE tablelinker SET client_encoding TO 'utf8';
ALTER ROLE tablelinker SET default_transaction_isolation TO 'read committed';
ALTER ROLE tablelinker SET timezone TO 'Asia/Tokyo';

CREATE database tablelinker;
GRANT ALL PRIVILEGES ON DATABASE tablelinker TO tablelinker;