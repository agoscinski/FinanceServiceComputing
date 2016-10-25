# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 17:08:29 2016

@author: Emely
"""

import orderclass
import _ctypes

"""matching algorithm using pro rata algorithm
@parameter:
    buy: list with buy orders
    sell: list with sell orders
    marketprice: actual markeprice
return void
set buy and sell shares to new amount"""
def match(buy, sell, marketprice):
    
    "Initialize lists for buy and sell with shares which can be traded"
    b=[]
    s=[]
    
    "get list with tradeable shares"
    for i in range(len(buy)):
        if(buy[i].qprice() == False):
            b = [b, buy[i]]
        elif(buy[i].getPrice() >= marketprice):
            b = [b, buy[i]]
            
    "get list with tradeable shares"
    for i in range(len(sell)):
        if(sell[i].qprice() == False):
            s = [s, sell[i]]
        elif(sell[i].getPrice() <= marketprice):
            s = [s, sell[i]]
            
    "get total volume of buy"
    volbuy = 0
    for i in range(1,len(b)):
        volbuy += b[i].getBuy()

    "get total volume of sell"
    volsell = 0
    for i in range(1,len(s)):
        volsell += s[i].getSell()

    "pro rata algorithm:"
    for i in range(1,len(s)):
        shares = 0
        shares = s[i].getSell() - (s[i].getSell()/volsell) * volbuy
        s[i].setSell(shares)
        
    for i in range(1,len(b)):
        shares = 0
        shares = b[i].getBuy() - (b[i].getBuy()/volbuy) * volsell
        b[i].setBuy(shares)
            
            