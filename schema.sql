CREATE DATABASE IF NOT EXISTS stock_db;
USE stock_db;



DROP TABLE IF EXISTS constituents;
DROP TABLE IF EXISTS OHLC;
DROP TABLE IF EXISTS indexes;
DROP TABLE IF EXISTS security;


CREATE TABLE indexes(
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `index_name` VARCHAR(50)
);


CREATE TABLE security(
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `sec_name` VARCHAR(255),
  `yahoo_ticker` VARCHAR(25)
);

CREATE TABLE constituents(
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `index_id` INTEGER,
  `sec_id` INTEGER,
  CONSTRAINT fk_indexes_constituents FOREIGN KEY(`index_id`) REFERENCES indexes(`id`),
  CONSTRAINT fk_security_constituents FOREIGN KEY(`sec_id`) REFERENCES security(`id`)
);

CREATE TABLE OHLC(
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `sec_id` INTEGER,
  `date` DATETIME,
  `open` FLOAT,
  `high` FLOAT,
  `low` FLOAT,
  `close` FLOAT,
  CONSTRAINT fk_security_ohlc FOREIGN KEY (`sec_id`) REFERENCES security(`id`)
);


CREATE TABLE top_picks(
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `date` DATETIME,
  `sec_id` INTEGER,
  `score` FLOAT,
  CONSTRAINT fk_top_picks_sec FOREIGN KEY(`sec_id`) REFERENCES security(`id`)
);
