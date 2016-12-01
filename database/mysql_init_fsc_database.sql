DROP SCHEMA IF EXISTS `FSCDatabase`;
CREATE SCHEMA IF NOT EXISTS `FSCDatabase` DEFAULT CHARACTER SET utf8 ;
USE `FSCDatabase`
-- create tables and structure
source database/init_fsc_database.sql

