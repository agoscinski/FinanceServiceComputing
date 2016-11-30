DROP SCHEMA IF EXISTS `TestFSCDatabase`;
CREATE SCHEMA IF NOT EXISTS `TestFSCDatabase` DEFAULT CHARACTER SET utf8 ;
USE `TestFSCDatabase`
-- create tables and structure
source tests/database/init_test_database.sql
