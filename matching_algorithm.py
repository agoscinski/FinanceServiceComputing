# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:13:40 2016

@author: Emely
"""


import numpy as np
import TradingClass


def pro_rata(buy, sell):
    """Matching algorithm using pro rata algorithm

    Args
        buy (list of TradingClass.Order):
        sell (list of TradingClass.Order):
    Returns:
    return trade matrix with traded shares
    set buy and sell shares to new amount"""

    if(len(buy)==0):
        return 0
        
    if(len(sell)==0):
        return 0
    
    
    lb = len(buy)
    ls = len(sell)
    
    "get total volume of buy"
    volbuy = 0
    for i in range(lb):
        volbuy += buy[i].get_order_qty()
        
    "get total volume of sell"
    volsell = 0
    for i in range(ls):
        volsell += sell[i].get_order_qty()
        
    "compare volumes"
    if(volsell>volbuy):
        dif = volsell - volbuy -1
        while(dif>0):
            dif = dif - sell[ls-1].get_order_qty()
            ls = ls-1

            
    summ = 0

    
    for i in range(ls):
        summ += buy[i].get_order_qty()*(i+1)

    
    "list of transactions, line is seller(i), row is buyer(j)"
    trade = np.zeros(shape=(len(sell), len(buy)))

    "time pro rata algorithm"
    p = []
    for i in range(lb):
        p.append((buy[i].get_order_qty()*buy[i].get_price()*(i+1))/summ)

    P = []
    for i in range(lb):
        comp = [buy[i].get_order_qty() * buy[i].get_price(), np.floor(p[i]*len(sell))]
        P.append(np.min(comp))
    
    for i in range(ls):
        while(sell[i].get_order_qty()>0):
            for j in range(lb):
                if P[j] > 0:
                    P[j] -= 1
                    buy[j].set_order_qty(buy[j].get_order_qty()-1)
                    sell[i].set_order_qty(sell[i].get_order_qty()-1)
                    trade[[i],[j]] += 1
                    if(sell[i].get_order_qty()==0):
                        break


    return trade


def match(orders):
    """This function takes a list of orders and returns the execution

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        order_executions (list of TradingClass.ExecutionReport)
    """
    buy_orders, sell_orders = extract_buy_and_sell_orders(orders)
    trading_matrix = pro_rata(buy_orders, sell_orders)
    order_executions = extract_order_executions_of_trading_matrix(trading_matrix)
    return order_executions


def extract_buy_and_sell_orders(orders):
    """This function takes a list of orders and returns one list with all buy orders, and one with all sell orders

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        buy_orders (list of TradingClass.ExecutionReport): Orders from type buy/bid
        sell_orders (list of TradingClass.ExecutionReport): Order from type sell/offer
    """
    buy_orders = []
    sell_orders = []
    for order in orders:
        if order.side == TradingClass.OrderSideType.BUY:
            buy_orders.append(order)
        elif order.side == TradingClass.OrderSideType.SELL:
            sell_orders.append(order)
    return buy_orders, sell_orders

def extract_order_executions_of_trading_matrix(trading_matrix):
    """Transforms a trading matrix to a list of buy and sell orders

    Args:
        trading_matrix (numpy.array): An array where in each row represents a sell order
            and each column represents one buy order

    Returns:
        orders (list of TradingClass.Order)
    """
    #it should care about virtual orders
    pass



# Encapsulate result of processing into execution report