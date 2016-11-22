# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:13:40 2016

@author: Emely
"""


import TradingClass
import numpy as np

"""matching algorithm using pro rata algorithm
    @parameter:
    buy: list with buy orders
    sell: list with sell orders
    marketprice: actual markeprice
return trade matrix with traded shares
set buy and sell shares to new amount"""
def pro_rata(buy, sell):
    
    lb = len(buy)
    ls = len(sell)
    
    "get total volume of buy"
    volbuy = 0
    for i in range(lb):
        volbuy += buy[i].get_order_qty()
        
    print(volbuy)
    "get total volume of sell"
    volsell = 0
    for i in range(ls):
        volsell += sell[i].get_order_qty()
        
    "compare volumes"
    while(volsell>volbuy):
        ls = ls-1
        for i in range(ls):
            volsell += sell[i].get_order_qty()
            
    print(volsell, volbuy)
        
        

    summ = 0

    
    for i in range(ls):
        if(lb>i):
            summ += buy[i].get_order_qty()*i


    "list of transactions, line is seller(i), row is buyer(j)"
    trade = np.zeros(shape=(len(sell), len(buy)))

    "time pro rata algorithm"
    p = []
    for i in range(ls):
        if(lb>i):
            p.append((buy[i].get_order_qty()*buy[i].get_price()*i)/summ)

    P = []
    for i in range(ls):
        if(lb>i):
            comp = [buy[i].get_order_qty()*buy[i].get_price(), np.ﬂoor(p[i]*len(sell))]
            P.append(np.min(comp))

    for i in range(ls):
        if(lb>i):
            while(sell[i].get_order_qty()>0):
                for j in range(ls):
                    if P[j] > 0:
                        P[j] -= 1
                        buy[j].set_order_qty(buy[j].get_order_qty()-1)
                        sell[i].set_order_qty(sell[i].get_order_qty()-1)
                        trade[[i],[j]] += 1


    return trade


def match(orders):
    """This function takes a list of orders and returns the execution

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        order_executions (list of TradingClass.OrderExecution)
    """
    buy, sell = extract_order
    trading_matrix = pro_rata(orders)
    order_executions = extract_order_executions_of_trading_matrix(trading_matrix)
    return order_executions


def extract_order_executions_of_trading_matrix(trading_matrix):
    """Transforms a trading matrix to a list of buy and sell orders

    Args:
        trading_matrix (numpy.array): An array where in each row represents a sell order
            and each column represents one buy order

    Returns:
        orders (list of TradingClass.orders)
    """
    #it should care about virtual orders
    pass



# Encapsulate result of processing into execution report
