# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:04:18 2016

@author: Emely
"""

import TradingClass
import matching_algorithm


class TestMatchingAlgorithm:
    def test_pro_rata(self):
        b1 = TradingClass.NewSingleOrder(1, 0, 0, 0, 0, 0, 0, 0, 120, 0, 200, 0, 0, 0, 0, 0)
        b2 = TradingClass.NewSingleOrder(2, 0, 0, 0, 0, 0, 0, 0, 180, 0, 220, 0, 0, 0, 0, 0)
        b3 = TradingClass.NewSingleOrder(3, 0, 0, 0, 0, 0, 0, 0, 100, 0, 190, 0, 0, 0, 0, 0)
        b4 = TradingClass.NewSingleOrder(4, 0, 0, 0, 0, 0, 0, 0, 50, 0, 180, 0, 0, 0, 0, 0)
        b5 = TradingClass.NewSingleOrder(5, 0, 0, 0, 0, 0, 0, 0, 560, 0, 210, 0, 0, 0, 0, 0)

        s6 = TradingClass.NewSingleOrder(6, 0, 0, 0, 0, 0, 0, 0, 90, 0, 230, 0, 0, 0, 0, 0)
        s7 = TradingClass.NewSingleOrder(7, 0, 0, 0, 0, 0, 0, 0, 230, 0, 230, 0, 0, 0, 0, 0)
        s8 = TradingClass.NewSingleOrder(8, 0, 0, 0, 0, 0, 0, 0, 40, 0, 180, 0, 0, 0, 0, 0)
        s9 = TradingClass.NewSingleOrder(9, 0, 0, 0, 0, 0, 0, 0, 600, 0, 170, 0, 0, 0, 0, 0)
        s10 = TradingClass.NewSingleOrder(10, 0, 0, 0, 0, 0, 0, 0, 140, 0, 200, 0, 0, 0, 0, 0)

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

