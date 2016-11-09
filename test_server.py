import server
import TradingClass
nasdaq_stock_ticker = "TESTTICKER"
nasdaq_stock = server.Stock(nasdaq_stock_ticker)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """

class TestStaticFunctions:

    def test_read_file(self):
        value = server.read_file("./test_file.txt")
        assert value == "word1;\nword2;\n"

class TestServerLogic:

    def test_pack_into_fix_market_data_response(self):
        market_data_required_id = '0'
        TradingClass.Order('0', 'GS', TradingClass.DateFix(2000,10,10), '1', 'TSLA', '1',
                 order_type, order_quantity, price, last_status)
        , md_entry_type_list, symbol, pending_stock_orders,
        stock_information
