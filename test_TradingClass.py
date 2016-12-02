import TradingClass


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

class TestGlobalFunctions:
    def test_get_values_from_fix_message_fields(self):
        pass

    def test_get_fix_group_field(self):
        pass
