DROP SCHEMA IF EXISTS `TestFSCDatabase`;
CREATE SCHEMA IF NOT EXISTS `TestFSCDatabase` DEFAULT CHARACTER SET utf8 ;
USE `TestFSCDatabase`
-- create structure and tables
source tests/database/init_test_database.sql
