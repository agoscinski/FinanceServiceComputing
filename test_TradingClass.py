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
        dummy_order.received_date = TradingClass.FIXDate.from_fix_date_stamp_string("20161120")
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

class TestOrderCancelRequest:

    def test_from_fix_message(self):
        #TODO yelinsheng test if the types are correct, similar to TestNewSingleOrder.test_from_fix_message
        dummy_order_cancel_request=TradingClass.OrderCancelRequest.create_dummy_order_cancel_request(orig_cl_ord_id="0")
        fix_message = dummy_order_cancel_request.to_fix_message()
        order_cancel_request=TradingClass.OrderCancelRequest.from_fix_message(fix_message)

        assert order_cancel_request.orig_cl_ord_id == "0"
        assert order_cancel_request.cl_ord_id == "0"
        assert order_cancel_request.symbol == "TSLA"
        assert order_cancel_request.side == TradingClass.FIXHandlerUtils.Side.BUY
        assert type(str(order_cancel_request.transact_time)) is str
        assert order_cancel_request.order_qty == 1000
        assert order_cancel_request.sender_comp_id == "GS"

class TestOrderCancelReject:

    def test_from_fix_message(self):
        #TODO yelinsheng
        dummy_order_cancel_reject=TradingClass.OrderCancelReject.create_dummy_order_cancel_reject()
        fix_message = dummy_order_cancel_reject.to_fix_message()
        order_cancel_reject=TradingClass.OrderCancelReject.from_fix_message(fix_message)

        assert order_cancel_reject.orig_cl_ord_id == "0"
        assert order_cancel_reject.cl_ord_id == "0"
        assert order_cancel_reject.order_id == "0"
        assert order_cancel_reject.ord_status == "0"
        assert order_cancel_reject.receiver_comp_id == "GS"

class TestNewSingleOrder:

    def test_from_fix_message(self):
        dummy_new_single_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        fix_message = dummy_new_single_order.to_fix_message()
        new_single_order = TradingClass.NewSingleOrder.from_fix_message(fix_message)
        assert type(new_single_order.client_order_id) is str
        assert type(new_single_order.handling_instruction) is str
        assert type(new_single_order.symbol) is str
        assert type(new_single_order.side) is str
        assert type(new_single_order.maturity_month_year) is TradingClass.FIXYearMonth
        assert type(new_single_order.maturity_day) is int
        assert type(new_single_order.transaction_time) is TradingClass.FIXDateTimeUTC
        assert type(new_single_order.order_quantity) is float
        assert type(new_single_order.order_type) is str
        assert type(new_single_order.price) is float



class TestClientOrder:
    def test_from_new_single_order(self):
        dummy_new_single_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        test_client_order=TradingClass.ClientOrder.from_new_single_order(dummy_new_single_order,2,101.,5)
        pass

