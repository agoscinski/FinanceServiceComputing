DROP SCHEMA IF EXISTS `TestClientDatabase`;
CREATE SCHEMA IF NOT EXISTS `TestClientDatabase` DEFAULT CHARACTER SET utf8 ;
USE `TestClientDatabase`
-- create tables and structure
source tests/database/client/init_test_client_database.sql
