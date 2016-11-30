import server
import TradingClass

nasdaq_stock_ticker = "TESTTICKER"
nasdaq_stock = server.Stock(nasdaq_stock_ticker)

fsc_server_database_handler = server.ServerDatabaseHandler(user_name="root", user_password="root",
                                                           database_name="TestFSCDatabase", database_port=3306,
                                                           init_database_script_path="./tests/database/init_test_database.sql")
server_config_file_name = "server.cfg"
fsc_server_logic = server.ServerLogic(server_config_file_name, fsc_server_database_handler)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    fsc_server_database_handler.init_database()



def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    fsc_server_database_handler.teardown_database()

class TestServerLogic:

    def test_create_execution_report_for_new_order(self):
        dummy_order = TradingClass.Order.create_dummy_order()
        fsc_server_logic.create_execution_report_for_new_order(dummy_order)


class TestServerDatabaseHandler:

    def test_extract_file_names_from_init_script(self):
        parsed_file_names = server.ServerDatabaseHandler.parse_file_names_from_init_script("tests/example_init_script.sql")
        asserted_file_names = ["tests/database/create_tables.sql",
                             "tests/database/create_view.sql",
                             "tests/database/account_insert.sql",
                             "tests/database/stock_insert.sql",
                             "tests/database/order_insert.sql",
                             "tests/database/order_execution_insert.sql"]
        assert parsed_file_names == asserted_file_names

    def test_parse_sql_commands_from_sql_file(self):
        parsed_sql_commands = server.ServerDatabaseHandler.parse_sql_commands_from_sql_file("tests/example_sql_commands.sql")
        asserted_sql_commands = ["SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0",
                                "CREATE TABLE IF NOT EXISTS `TestFSCDatabase`.`Stock` (  `Ticker` VARCHAR(6) NOT NULL,  `CompanyName` VARCHAR(45) NULL,  `LotSize` INT NULL,  `TickSize` DECIMAL(20,2) NULL,  `TotalVolume` INT NULL,  PRIMARY KEY (`Ticker`))ENGINE = InnoDB",
                                "INSERT INTO Stock(Ticker, CompanyName, LotSize, TickSize, TotalVolume) VALUES('MS','Morgan Stanley','100','0.01','10000000')"]
        assert parsed_sql_commands[0] == asserted_sql_commands[0]
        assert parsed_sql_commands[1] == asserted_sql_commands[1]
        assert parsed_sql_commands[2] == asserted_sql_commands[2]

    def test_insert_order(self):
        dummy_order = TradingClass.Order.create_dummy_order()
        fsc_server_database_handler.insert_order(dummy_order)

    def test_fetch_pending_orders_for_stock_ticker(self):
        symbol = "TSLA"
        order_list = fsc_server_database_handler.fetch_pending_orders_for_stock_ticker(symbol)
        goldmann_sachs_order = TradingClass.Order(client_order_id='0',account_company_id='GS', received_date=TradingClass.FIXDate.from_mysql_date_stamp_string('2016-11-09'), handling_instruction='1',maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string('2016-11-15'),stock_ticker='TSLA', side='1',order_type='2',order_quantity='1000',price='10000', last_status='1')
        morgan_stanley_order = TradingClass.Order(client_order_id='0',account_company_id='MS', received_date=TradingClass.FIXDate.from_mysql_date_stamp_string('2016-11-08'), handling_instruction='1',maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string('2016-11-11'),stock_ticker='TSLA', side='2',order_type='2',order_quantity='200',price='1005', last_status='1')
        order_list.__contains__(goldmann_sachs_order)
        order_list.__contains__(morgan_stanley_order)
        assert order_list


