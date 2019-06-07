CREATE DATABASE IF NOT EXISTS test;
USE test;
grant all on test.* to 'user' identified by 'userpass';

ALTER DATABASE test CHARACTER SET utf8 COLLATE utf8_general_ci;

-- mediumblob ~ 16mb
-- utf8 for every text column
CREATE TABLE IF NOT EXISTS incoming_people (
         id    INT UNSIGNED  NOT NULL AUTO_INCREMENT,
         name         VARCHAR(30)   CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
         file_name         VARCHAR(30)   CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
         file_data         MEDIUMBLOB,
         PRIMARY KEY  (id));
