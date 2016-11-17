# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:14:48 2016

@author: Emely
"""

class Order:
    
    """Constructor of class Order:
	0 means that any price is okay
        @Parameter:
            id: ID of client
            buy: quantity of shares to buy; default 0
            sell: quantity of shares to sell; default 0
            price: minimum price to sell or maximum price to buy; 
            default 0 means marketprice"""
    def __init__(self, id, buy=0, sell=0, price=0):
        
        self.Id = id
        self.Buy = buy
        self.Sell = sell
        self.Price = price
        
    "return price"
    def getId(self):
        return self.Id
        
    "returns amount of shares to buy"    
    def getBuy(self):
        return self.Buy
        
    "returns amount of shares to sell"    
    def getSell(self):
        return self.Sell
        
    "returns pricelimit on order"    
    def getPrice(self):
        return self.Price
        
    "returns true if it is a buy order"
    def qbuy(self):
        if self.Buy>0:
            return True
        else:
            return False
            
    "returns true if it is a sell order"
    def qsell(self):
        if self.Sell>0:
            return True
        else:
            return False
            
    "returns true if a pricelimit exists"
    def qprice(self):
        if self.Price>0:
            return True
        else:
            return False
