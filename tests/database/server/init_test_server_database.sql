-- create tables and dependencies
source tests/database/server/create_tables.sql
-- create views
source database/server/create_views.sql
-- insert data
source database/server/account_role_inserts.sql
source database/server/account_inserts.sql
source database/server/stock_inserts.sql
source database/server/order_inserts.sql
source database/server/order_execution_inserts.sql
source database/server/order_cancel_inserts.sql
