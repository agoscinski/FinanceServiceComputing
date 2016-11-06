# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:14:48 2016

@author: Emely
"""

class Order(object):
    
    """Constructor of class Order:
        @Parameter:
            id: ID of client
            buy: amount of shares to buy; default 0
            sell: amount of shares to sell; default 0
            price: minimum price to sell or maximum price to buy; 
            default 0 means marketprice"""
    def __init__(self, id, buy=0, sell=0, price=0):
        
        self.__Id = id
        self.__Buy = buy
        self.__Sell = sell
        self.__Price = price
        
    "return price"
    def getId(self):
        return self.__Id
        
    "returns amount of shares to buy"    
    def getBuy(self):
        return self.__Buy
        
    "returns amount of shares to sell"    
    def getSell(self):
        return self.__Sell
        
    "returns pricelimit on order"    
    def getPrice(self):
        return self.__Price
        
    "sets new amount of shares to buy"
    def setBuy(self, shares):
        self.__Buy = shares
        
    "sets new amount of shares to sell"
    def setSell(self, shares):
        self.__Sell = shares
        
    "returns true if it is a buy order"
    def qbuy(self):
        if self.__Buy>0:
            return True
        else:
            return False
            
    "returns true if it is a sell order"
    def qsell(self):
        if self.__Sell>0:
            return True
        else:
            return False
            
    "returns true if a pricelimit exists"
    def qprice(self):
        if self.__Price>0:
            return True
        else:
            return False