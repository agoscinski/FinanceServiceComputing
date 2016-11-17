# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:13:40 2016

@author: Emely
"""

import numpy as np
import TradingClass
import quickfix as fix

"""matching algorithm using pro rata algorithm
    @parameter:
    buy: list with buy orders
    sell: list with sell orders
    marketprice: actual markeprice
    return void
    set buy and sell shares to new amount
"""


def pro_rata(buy, sell):
    "get total volume of buy"
    volume_of_buy = 0
    for i in range(len(buy)):
        volume_of_buy += buy[i].getBuy()

    "get total volume of sell"
    volume_of_sell = 0
    for i in range(len(sell)):
        volume_of_sell += sell[i].getSell()

    sum = 0

    for i in range(len(sell)):
        if (len(buy) > i):
            sum += buy[i].getBuy() * i

    "list of transactions, line is seller(i), row is buyer(j)"
    trade = np.zeros(shape=(len(sell), len(sell)))

    "time pro rata algorithm"
    p = []
    for i in range(len(sell)):
        if (len(buy) > i):
            p.append((buy[i].getBuy() * buy[i].getPrice() * i) / sum)

    P = []
    for i in range(len(sell)):
        if (len(buy) > i):
            comp = [buy[i].getBuy() * buy[i].getPrice(), np.floor(p[i] * len(sell))]
            P.append(np.min(comp))

    for i in range(len(sell)):
        if (len(buy) > i):
            while (sell[i].getSell() > 0):
                for j in range(len(sell)):
                    if P[j] > 0:
                        P[j] -= 1
                        buy[j].setBuy(buy[j].getBuy() - 1)
                        sell[i].setSell(sell[i].getSell() - 1)
                        trade[[i], [j]] += 1

    return trade


def match(orders):
    """This function takes a list of orders and returns the execution

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        order_executions (list of TradingClass.OrderExecution)
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
        buy_orders (list of TradingClass.OrderExecution): Orders from type buy/bid
        sell_orders (list of TradingClass.OrderExecution): Order from type sell/offer
    """
    buy_orders = []
    sell_orders = []
    for order in orders:
        if order.side == TradingClass.FIXHandler.SIDE_BUY:
            buy_orders.append(order)
        elif order.side == TradingClass.FIXHandler.SIDE_SELL:
            sell_orders.append(order)
    return buy_orders, sell_orders

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