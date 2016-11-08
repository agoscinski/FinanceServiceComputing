# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:04:18 2016

@author: Emely
"""

"""py.test for matching algorithm"""

import numpy as np
import orderclass
import matchAlg2

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

assert len(matchAlg2.match([],[]))==0
assert len(matchAlg2.match([], s))==len(s)
assert len(matchAlg2.match(b,[]))==0