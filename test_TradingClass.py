import TradingClass


def setup_module(module):
    """ setup any state specific to the execution of the given module."""


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """


class TestOrder:
    def test_create_dummy_order(self):
        TradingClass.Order.create_dummy_order()


class TestGlobalFunctions:
    def test_get_values_from_fix_message_fields(self):
        pass

    def test_get_fix_group_field(self):
        pass
