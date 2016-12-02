# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:13:40 2016

@author: Emely
"""

import numpy as np
import TradingClass


def pro_rata(buy_orders, sell_orders):
    """Matching algorithm using pro rata algorithm

    Require: buy and sell orders shall not been matured yet

    Args:
        buy_orders (list of TradingClass.Order):
        sell_orders (list of TradingClass.Order):
    Returns:
        rade_matrix (numpy.array): matrix for traded shares set buy and sell shares to new amount"""

    if len(buy_orders) == 0 or len(sell_orders) == 0: return None

    current_buy_orders_length = len(buy_orders)
    current_sell_orders_length = len(sell_orders)

    # get total volume of buy
    volume_buy = 0
    for i in range(current_buy_orders_length):
        volume_buy += buy_orders[i].cumulative_order_quantity

    # get total volume of sell
    volume_sell = 0
    for i in range(current_sell_orders_length):
        volume_sell += sell_orders[i].cumulative_order_quantity

    # compare volumes
    if volume_sell > volume_buy:
        sell_buy_diff = volume_sell - volume_buy - 1
        while sell_buy_diff > 0:
            sell_buy_diff -= sell_orders[current_sell_orders_length - 1].cumulative_order_quantity
            current_sell_orders_length -= 1

    sum_of_weighted_orders = 0

    for i in range(current_sell_orders_length):
        sum_of_weighted_orders += buy_orders[i].cumulative_order_quantity * (i + 1)

    # list of transactions, line is seller(i), row is buyer(j)
    trade_matrix = np.zeros(shape=(len(sell_orders), len(buy_orders)))

    # time pro rata algorithm
    p = []
    for i in range(current_buy_orders_length):
        p.append((buy_orders[i].cumulative_order_quantity * buy_orders[i].price * (i + 1)) / sum_of_weighted_orders)

    P = []
    for i in range(current_buy_orders_length):
        comp = [buy_orders[i].cumulative_order_quantity * buy_orders[i].price, np.floor(p[i] * current_sell_orders_length)]
        P.append(np.min(comp))

    for i in range(current_sell_orders_length):
        while sell_orders[i].cumulative_order_quantity > 0:
            for j in range(current_buy_orders_length):
                if P[j] > 0:
                    P[j] -= 1
                    buy_orders[j].cumulative_order_quantity -= 1
                    sell_orders[i].cumulative_order_quantity -= 1
                    trade_matrix[[i], [j]] += 1
                    if sell_orders[i].cumulative_order_quantity == 0:
                        break

    return trade_matrix


def match(orders):
    """This function takes a list of orders and returns the execution

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        order_executions (list of TradingClass.ExecutionReport)
    """
    buy_orders, sell_orders = extract_buy_and_sell_orders(orders)
    trading_matrix = pro_rata(buy_orders, sell_orders)
    order_executions = extract_order_executions_out_of_trading_matrix(trading_matrix)
    return order_executions


# TODO sorting to latest is order is oldest order
# TODO change MARKET_ORDERS to 1 for sell and float max for buy
def extract_buy_and_sell_orders(orders):
    """This function takes a list of orders and returns one list with all buy orders, and one with all sell orders

    Args:
        orders (list of TradingClass.Order): These are the are orders the algorithm received

    Returns:
        buy_orders (list of TradingClass.ExecutionReport): Orders from type buy/bid
        sell_orders (list of TradingClass.ExecutionReport): Orders from type sell/offer
    """
    buy_orders = []
    sell_orders = []
    for order in orders:
        if order.side == TradingClass.DatabaseHandlerUtils.Side.BUY:
            buy_orders.append(order)
        elif order.side == TradingClass.DatabaseHandlerUtils.Side.SELL:
            sell_orders.append(order)
    return buy_orders, sell_orders


def extract_order_executions_out_of_trading_matrix(trading_matrix, buy_orders, sell_orders):
    """Transforms a trading matrix to a list of buy and sell orders

    Function requires number of rows trading_matrix is the same as the length of sell_orders
    and number of columns trading_matrix is the same as the length of buy_orders.
    Function requires only buy orders are in the buy_orders list and only sell orders are in the
    sell_orders list

    Args:
        trading_matrix (numpy.array): An array where in each row represents a sell order
            and each column represents one buy order
        buy_orders (list of TradingClass.Order): A list of buy orders related to the trading_matrix
        sell_orders (list of TradingClass.Order): A list of sell orders related to the trading_matrix

    Returns:
        order_executions (list of TradingClass.OrderExecution)
    """
    execution_orders = []
    current_timestamp = TradingClass.FIXDateTimeUTC.create_for_current_time()
    for i in trading_matrix.shape[0]:
        for j in trading_matrix.shape[1]:
            execution_order = create_order_execution_from_trading_matrix_entry(trading_matrix[i, j], buy_orders[j],
                                                                               sell_orders[i], current_timestamp)
            execution_orders.append(execution_order)

    return execution_orders


class MatchingError(object):
    pass


def create_order_execution_from_trading_matrix_entry(trading_matrix_entry, buy_order, sell_order, timestamp):
    """Creates an order execution from an entry in a trading matrix

    Args:
        trading_matrix_entry (float): An array where in each row represents a sell order
            and each column represents one buy order
        buy_order (TradingClass.Order): order from type buy/bid
        sell_order (TradingClass.Order): order from type sell/offer
        timestamp (TradingClass.FIXDateTimeUTC): timestamp for the order execution

    Returns:
        order_execution (TradingClass.OrderExecution)
    """
    matched_price = determine_price_for_match(buy_order, sell_order)
    execution_order = TradingClass.OrderExecution.from_buy_and_sell_order(executed_quantity=trading_matrix_entry,
                                                                          executed_price=matched_price,
                                                                          buy_order=buy_order,
                                                                          sell_order=sell_order,
                                                                          execution_time=timestamp)
    return execution_order


# TODO two market orders should be matched on current market price, otherwise it only makes sense create exetreme high prices for market orders, to get higher value;
# TODO solution: current take market price for two market orders
def determine_price_for_match(buy_order, sell_order):
    """Determines the price between a buy and sell order which has been matched

    If between a sell and buy order price is an intersection they can agree on, then the price in the middle will be
    determined. If there is no intersection but both orders are market order then still the price in the middle will
    be determined. If there is no intersection and only one order is a limit order, then the price of the limit order
    determines the price. If there is not intersection and both order are limite order, then an error will be outputted

    Args:
        buy_order (TradingClass.Order): order from type buy/bid
        sell_order (TradingClass.Order): order from type sell/offer

    Returns:
        matched_price (float): the price on which buyer and seller will agree on
    """

    is_intersection = buy_order.price >= sell_order.price
    if is_intersection:
        return sell_order.price + (buy_order.price - sell_order.price) / 2.
    elif buy_order.order_type == TradingClass.DatabaseHandlerUtils.OrderType.MARKET and sell_order.order_type == TradingClass.DatabaseHandlerUtils.OrderType.MARKET:
        return buy_order.price + (sell_order.price - buy_order.price) / 2.
    elif buy_order.order_type == TradingClass.DatabaseHandlerUtils.OrderType.LIMIT and sell_order.order_type == TradingClass.DatabaseHandlerUtils.OrderType.LIMIT:
        raise MatchingError("Matched orders have no intersection in price and are both limit orders.")
    else:
        # the state is only one order is a limit order
        limit_order = buy_order if buy_order.order_id == TradingClass.DatabaseHandlerUtils.OrderType.LIMIT else sell_order
        return limit_order.price
