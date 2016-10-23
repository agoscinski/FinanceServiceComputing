# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 17:08:29 2016

@author: Emely
"""

import orderclass

"""matching algorithm using pro rata algorithm
@parameter:
    buy: list with buy orders
    sell: list with sell orders
    marketprice: actual markeprice
return void
set buy and sell shares to new amount"""
def match(buy, sell, marketprice):
    
    "Initialize lists for buy and sell with shares which can be traded"
    b=[], s=[]
    
    "get list with tradeable shares"
    for i in range(len(buy)):
        if(buy[i].qprice == False):
            b.add(buy[i])
        elif(buy[i].getPrice >= marketprice):
            b.add(buy[i])
            
    "get list with tradeable share"
    for i in range(len(sell)):
        if(sell[i].qprice == False):
            s.add(sell[i])
        elif(sell[i].getPrice <= marketprice):
            s.add(sell[i])
            
    "get total volume of buy"
    volbuy = 0
    for i in range(len(b)):
        volbuy += b[i].getBuy

    "get total volume of sell"
    volsell = 0
    for i in range(len(s)):
        volsell += s[i].getSell

    "pro rata algorithm:"
    for i in range(len(s)):
        shares = 0
        shares = s[i].getSell - (s[i].getSell/volsell) * volbuy
        s[i].setSell(shares)
        
    for i in range(len(b)):
        shares = 0
        shares = b[i].getBuy - (b[i].getBuy/volbuy) * volsell
        b[i].setBuy(shares)
            
            