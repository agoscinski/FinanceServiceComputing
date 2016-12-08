import client
import TradingClass

client_config_file_name = "client.cfg"
fsc_client_logic = client.ClientLogic(client_config_file_name)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    fsc_client_logic.client_fix_handler.connect_to_server()


class TestClientLogic:

    def test_process_new_single_order_request(self):
        dummy_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        fsc_client_logic.process_new_single_order_request(dummy_order.symbol, dummy_order.side, dummy_order.order_type, dummy_order.price, dummy_order.order_quantity)
