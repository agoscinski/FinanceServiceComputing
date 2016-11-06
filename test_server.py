import server

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
