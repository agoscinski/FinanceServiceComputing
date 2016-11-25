# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:32:20 2016

@author: Emely
"""

import TradingClass
import matching_algorithm

def test_pro_rata():
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

        assert (matching_algorithm.pro_rata([], [])) == 0
        assert (matching_algorithm.pro_rata([], s)) == 0
        assert (matching_algorithm.pro_rata(b, [])) == 0

        print(matching_algorithm.pro_rata(b,s))