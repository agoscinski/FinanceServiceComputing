import client
import datetime
import TradingClass

client_application_id = "test"
fsc_client_logic = client.ClientLogic(client_application_id)
fsc_client_database_handler = client.ClientDatabaseHandler(application_id="test_client", database_host="localhost",
    user_name="root", user_password="root", database_name="TestClientDatabase", database_port=3306,
    init_database_script_path="./tests/database/client/init_test_client_database.sql")

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    fsc_client_database_handler.init_database()


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    fsc_client_database_handler.teardown_database()


class TestClientLogic:

    def test_process_new_single_order_request(self):
        pass

    def test_get_tomorrows_maturity_date(self):
        test_date,test_day = fsc_client_logic.get_tomorrows_maturity_date()
        tomorrow_datetime=datetime.date.today() + datetime.timedelta(days=1)
        assert test_date == TradingClass.FIXYearMonth(tomorrow_datetime)
        assert test_day == tomorrow_datetime.day

    #def test_process_new_single_order_request(self):
    #    dummy_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
    #    fsc_client_logic.process_new_single_order_request(dummy_order.symbol, dummy_order.side, dummy_order.order_type, dummy_order.price, dummy_order.order_quantity)


class TestClientDatabaseHandler:

    def test_insert_order(self):
        dummy_order = TradingClass.ClientOrder.create_dummy_client_order()
        assert fsc_client_database_handler.insert_order(dummy_order) == None
        pass