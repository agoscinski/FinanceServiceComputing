DROP SCHEMA IF EXISTS `ServerDatabase`;
CREATE SCHEMA IF NOT EXISTS `ServerDatabase` DEFAULT CHARACTER SET utf8 ;
USE `ServerDatabase`
-- create tables and structure
source database/server/init_server_database.sql

