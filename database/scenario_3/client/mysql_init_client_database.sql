DROP SCHEMA IF EXISTS `ClientDatabase`;
CREATE SCHEMA IF NOT EXISTS `ClientDatabase` DEFAULT CHARACTER SET utf8 ;
USE `ClientDatabase`
-- create tables and structure
source database/client/init_client_database.sql
