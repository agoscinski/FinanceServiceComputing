# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:32:20 2016

@author: Emely
"""

import TradingClass
import matching_algorithm

def test_pro_rata():
        b1 = TradingClass.Order(1, 0, 0, 0, 0, 0, 0, 120, 200, 0, 0, 0, 0, 0)
        b2 = TradingClass.Order(2, 0, 0, 0, 0, 0, 0, 180, 220, 0, 0, 0, 0, 0)
        b3 = TradingClass.Order(3, 0, 0, 0, 0, 0, 0, 100, 190, 0, 0, 0, 0, 0)
        b4 = TradingClass.Order(4, 0, 0, 0, 0, 0, 0, 50, 180, 0, 0, 0, 0, 0)
        b5 = TradingClass.Order(5, 0, 0, 0, 0, 0, 0, 560, 210, 0, 0, 0, 0, 0)

        s6 = TradingClass.Order(6, 0, 0, 0, 0, 0, 0, 90, 230, 0, 0, 0, 0, 0)
        s7 = TradingClass.Order(7, 0, 0, 0, 0, 0, 0, 230, 230, 0, 0, 0, 0, 0)
        s8 = TradingClass.Order(8, 0, 0, 0, 0, 0, 0, 40, 180, 0, 0, 0, 0, 0)
        s9 = TradingClass.Order(9, 0, 0, 0, 0, 0, 0, 600, 170, 0, 0, 0, 0, 0)
        s10 = TradingClass.Order(10, 0, 0, 0, 0, 0, 0, 140, 200, 0, 0, 0, 0, 0)

        b = [b1, b2, b3, b4, b5]

        s = [s6, s7, s8, s9, s10]

        assert (matching_algorithm.pro_rata([], [])) == 0
        assert (matching_algorithm.pro_rata([], s)) == 0
        assert (matching_algorithm.pro_rata(b, [])) == 0

        print(matching_algorithm.pro_rata(b,s))