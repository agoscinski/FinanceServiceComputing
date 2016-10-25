# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:29:37 2016

@author: Emely
"""

import orderclass
import matchAlg

b1 = orderclass.Order(1, 20, 0 , 14)
b2 = orderclass.Order(2, 27, 0 , 56)
b3 = orderclass.Order(3, 42, 0, 0)
b4 = orderclass.Order(4, 24, 0 , 89)
b5 = orderclass.Order(5, 89, 0, 3)
b6 = orderclass.Order(6, 0, 78, 5)
b7 = orderclass.Order(7, 0, 6, 34)
b8 = orderclass.Order(8, 0, 1, 0)
b9 = orderclass.Order(9, 0,  104, 7)
b10 = orderclass.Order(10, 0, 45, 50)


b = [b1, b2, b3, b4, b5]
s = [b6, b7, b8, b9, b10]

matchAlg.match(b,s,30)
print(b)
print(s)