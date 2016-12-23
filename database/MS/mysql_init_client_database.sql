DROP SCHEMA IF EXISTS `MSDatabase`;
CREATE SCHEMA IF NOT EXISTS `MSDatabase` DEFAULT CHARACTER SET utf8 ;
USE `MSDatabase`
-- create tables and structure
source database/MS/init_client_database.sql
