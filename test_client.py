import client
import TradingClass

client_config_file_name = "client.cfg"
fsc_client_logic = client.ClientLogic(client_config_file_name)
fsc_client_database_handler = client.ClientDatabaseHandler(user_name="root", user_password="root",
                                                           database_name="TestClientDatabase", database_port=3306,
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

    #def test_process_new_single_order_request(self):
    #    dummy_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
    #    fsc_client_logic.process_new_single_order_request(dummy_order.symbol, dummy_order.side, dummy_order.order_type, dummy_order.price, dummy_order.order_quantity)


class TestClientDatabaseHandler:

    def test_insert_order(self):
        dummy_order = TradingClass.ClientOrder.create_dummy_client_order()
        fsc_client_database_handler.insert_order(dummy_order)