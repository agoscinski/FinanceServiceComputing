DROP SCHEMA IF EXISTS `TestServerDatabase`;
CREATE SCHEMA IF NOT EXISTS `TestServerDatabase` DEFAULT CHARACTER SET utf8 ;
USE `TestServerDatabase`
-- create tables and structure
source tests/database/server/init_test_server_database.sql
