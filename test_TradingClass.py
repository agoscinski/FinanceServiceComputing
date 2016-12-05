import TradingClass
import numpy as np


def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """

class TestExecutionReport:

    def test_from_order(self):
        dummy_order = TradingClass.Order.create_dummy_order()
        left_quantity = dummy_order.order_quantity
        cumulative_quantity = 0
        average_price = 0
        TradingClass.ExecutionReport.from_order(dummy_order, TradingClass.FIXHandlerUtils.ExecutionTransactionType.NEW,
                                                TradingClass.FIXHandlerUtils.ExecutionType.NEW,
                                                TradingClass.FIXHandlerUtils.OrderStatus.NEW, left_quantity,
                                                cumulative_quantity, average_price)
class TestNewSingleOrder:

    def test_create_dummy_new_single_order(self):
        TradingClass.NewSingleOrder.create_dummy_new_single_order()


class TestOrder:

    def test_from_new_single_order(self):
        dummy_new_single_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        TradingClass.Order.from_new_single_order(dummy_new_single_order)

    def test_create_dummy_order(self):
        TradingClass.Order.create_dummy_order()

    def test_order_id(self):
        dummy_order = TradingClass.Order.create_dummy_order()
        dummy_order.client_order_id = "20161120-001"
        dummy_order.account_company_id = "client"
        dummy_order.received_time = TradingClass.FIXDate.from_fix_date_stamp_string("20161120")
        assert dummy_order.order_id == "20161120-001_client_20161120"

class TestClientLogicUtils:

    def test_extract_n_smallest_indices(self):
        four_smallest_indices = TradingClass.ClientLogicUtils.extract_n_smallest_indices([2, 3, 5, 1, 6, 10], 4)
        assert [3, 0, 1, 2] == list(four_smallest_indices)

    def test_extract_n_biggest_indices(self):
        four_smallest_indices = TradingClass.ClientLogicUtils.extract_n_biggest_indices([2, 3, 5, 1, 6, 10], 4, order="descending")
        assert [5,4,2,1] == list(four_smallest_indices)

    def test_get_values_from_lists_for_certain_indices(self):
        values = TradingClass.ClientLogicUtils.get_values_from_lists_for_certain_indices([0,5,1,3], [0,1,2,3,4,5,6,7], [3,2,1,5,100,10])
        assert values[0] == [0,5,1,3] and values[1] == [3,10,2,5]

    def test_transform_numpy_array_to_list(self):
        numpy_arrays = (np.array([1,1,2]) , np.array([1]))
        lists = TradingClass.ClientLogicUtils.transform_numpy_array_to_list(*numpy_arrays)
        assert type(lists[0]) == type([]) and type(lists[1]) == type([])


class TestDatabaseHandler:
    def test_extract_file_names_from_init_script(self):
        parsed_file_names = TradingClass.DatabaseHandlerUtils.parse_file_names_from_init_script(
            "tests/example_init_script.sql")
        asserted_file_names = ["tests/database/create_tables.sql",
                               "tests/database/create_view.sql",
                               "tests/database/account_insert.sql",
                               "tests/database/stock_insert.sql",
                               "tests/database/order_insert.sql",
                               "tests/database/order_execution_insert.sql"]
        assert parsed_file_names == asserted_file_names

    def test_parse_sql_commands_from_sql_file(self):
        parsed_sql_commands = TradingClass.DatabaseHandlerUtils.parse_sql_commands_from_sql_file(
            "tests/example_sql_commands.sql")
        asserted_sql_commands = ["SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0",
                                 "CREATE TABLE IF NOT EXISTS `TestFSCDatabase`.`Stock` (   `Ticker` VARCHAR(6) NOT NULL,   `CompanyName` VARCHAR(45) NULL,   `LotSize` INT NULL,   `TickSize` DECIMAL(20,2) NULL,   `TotalVolume` INT NULL,   PRIMARY KEY (`Ticker`)) ENGINE = InnoDB",
                                 "INSERT INTO Stock(Ticker, CompanyName, LotSize, TickSize, TotalVolume) VALUES('MS','Morgan Stanley','100','0.01','10000000')"]
        assert parsed_sql_commands[0] == asserted_sql_commands[0]
        assert parsed_sql_commands[1] == asserted_sql_commands[1]
        assert parsed_sql_commands[2] == asserted_sql_commands[2]

class TestGlobalFunctions:
    def test_get_values_from_fix_message_fields(self):
        pass

    def test_get_fix_group_field(self):
        pass
