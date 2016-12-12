import matching_algorithm
import TradingClass
import timeit

def run_pro_rata(number_of_orders):
    buy_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=12000., price=200.)
    sell_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=12000., price=200.)
    buy_orders = [buy_order for _ in range(number_of_orders)]
    sell_orders = [sell_order for _ in range(number_of_orders)]
    matching_algorithm.pro_rata(buy_orders, sell_orders)

def time_tests():
    t = timeit.Timer("run_pro_rata(1)", number=1, setup="from matching_algorithm_time_test import run_pro_rata")
    t.timeit()