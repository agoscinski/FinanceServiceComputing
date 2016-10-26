import server

nasdaq_stock_ticker = "TESTTICKER"
nasdaq_stock = server.Stock(nasdaq_stock_ticker)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    server.ServerDatabaseHandler().delete_stock_data(nasdaq_stock)

class TestMarketSimulator:
    market_simulation_handler = server.MarketSimulationHandler()
    market_simulation_handler.stock_list = [nasdaq_stock_ticker]

    def test_load_market_data_into_database(self):
        self.market_simulation_handler.load_market_data_into_database()
