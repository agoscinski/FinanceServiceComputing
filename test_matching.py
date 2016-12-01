# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:04:18 2016

@author: Emely
"""

import TradingClass
import matching_algorithm


class TestMatchingAlgorithm:
    def test_pro_rata(self):
        b1 = TradingClass.Order(1, 0, 0, 0, 0, 0, 0, 120, 200, 0, 0, 0, 0, 0)
        b2 = TradingClass.Order(2, 0, 0, 0, 0, 0, 0, 180, 220, 0, 0, 0, 0, 0)
        b3 = TradingClass.Order(3, 0, 0, 0, 0, 0, 0, 100, 190, 0, 0, 0, 0, 0)
        b4 = TradingClass.Order(4, 0, 0, 0, 0, 0, 0, 50, 180, 0, 0, 0, 0, 0)
        b5 = TradingClass.Order(5, 0, 0, 0, 0, 0, 0, 560, 210, 0, 0, 0, 0, 0)

        s6 = TradingClass.Order(6, 0, 0, 0, 0, 0, 0, 0, 90, 230, 0, 0, 0, 0, 0)
        s7 = TradingClass.Order(7, 0, 0, 0, 0, 0, 0, 0, 230, 230, 0, 0, 0, 0, 0)
        s8 = TradingClass.Order(8, 0, 0, 0, 0, 0, 0, 0, 40, 180, 0, 0, 0, 0, 0)
        s9 = TradingClass.Order(9, 0, 0, 0, 0, 0, 0, 0, 600, 170, 0, 0, 0, 0, 0)
        s10 = TradingClass.Order(10, 0, 0, 0, 0, 0, 0, 0, 140, 200, 0, 0, 0, 0, 0)

        b = [b1, b2, b3, b4, b5]

        s = [s6, s7, s8, s9, s10]

        assert len(matching_algorithm.pro_rata([], [])) == 0
        assert len(matching_algorithm.pro_rata([], s)) == 0
        assert len(matching_algorithm.pro_rata(b, [])) == 0
        #TODO scenarios: 4,2 match perfectly, matched partially, only one 1 quantity


    def test_extract_buy_and_sell_orders(self):
        dummy_orders = []
        for i in range(5):
            dummy_orders.append(TradingClass.Order.create_dummy_order())
        dummy_orders[0].side = TradingClass.OrderSideType.SELL
        dummy_orders[1].side = TradingClass.OrderSideType.BUY
        dummy_orders[2].side = TradingClass.OrderSideType.SELL
        dummy_orders[3].side = TradingClass.OrderSideType.BUY
        dummy_orders[4].side = TradingClass.OrderSideType.SELL
        buy_orders, sell_orders = matching_algorithm.extract_buy_and_sell_orders(dummy_orders)
        assert buy_orders[0] == dummy_orders[1]
        assert buy_orders[1] == dummy_orders[3]
        assert sell_orders[0] == dummy_orders[0]
        assert sell_orders[1] == dummy_orders[2]
        assert sell_orders[2] == dummy_orders[4]

