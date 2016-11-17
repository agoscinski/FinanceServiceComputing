# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:04:18 2016

@author: Emely
"""

"""py.test for matching algorithm"""

import numpy as np
import TradingClass
import orderclass
import matching_algorithm
import quickfix as fix


class TestMatchingAlgorithm:
    def test_pro_rata(self):
        b1 = orderclass.Order(1, 28, 0, 42)
        b2 = orderclass.Order(2, 27, 0, 36)
        b3 = orderclass.Order(3, 42, 0, 756)
        b4 = orderclass.Order(4, 24, 0, 45)
        b5 = orderclass.Order(5, 89, 0, 86)

        s6 = orderclass.Order(6, 0, 100, 35)
        s7 = orderclass.Order(7, 0, 6, 7)
        s8 = orderclass.Order(8, 0, 1, 103)
        s9 = orderclass.Order(9, 0, 104, 15)
        s10 = orderclass.Order(10, 0, 45, 12)

        b = [b1, b2, b3, b4, b5]

        s = [s6, s7, s8, s9, s10]

        assert len(matching_algorithm.pro_rata([], [])) == 0
        assert len(matching_algorithm.pro_rata([], s)) == len(s)
        assert len(matching_algorithm.pro_rata(b, [])) == 0
        #TODO scenarios: 4,2 match perfectly, matched partially, only one 1 quantity


    def test_extract_buy_and_sell_orders(self):
        dummy_orders = []
        for i in range(5):
            dummy_orders.append(TradingClass.Order.create_dummy_order())
        dummy_orders[0].side = TradingClass.FIXHandler.SIDE_SELL
        dummy_orders[1].side = TradingClass.FIXHandler.SIDE_BUY
        dummy_orders[2].side = TradingClass.FIXHandler.SIDE_SELL
        dummy_orders[3].side = TradingClass.FIXHandler.SIDE_BUY
        dummy_orders[4].side = TradingClass.FIXHandler.SIDE_SELL
        buy_orders, sell_orders = matching_algorithm.extract_buy_and_sell_orders(dummy_orders)
        assert buy_orders[0] == dummy_orders[1]
        assert buy_orders[1] == dummy_orders[3]
        assert sell_orders[0] == dummy_orders[0]
        assert sell_orders[1] == dummy_orders[2]
        assert sell_orders[2] == dummy_orders[4]

