# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:04:18 2016

@author: Emely
"""

import TradingClass
import matching_algorithm


class TestMatchingAlgorithm:
    """
    def test_pro_rata(self):
        b1 = TradingClass.NewSingleOrder(1, 0, 0, 0, 0, 0, 0, 0, 120, 0, 200, 0, 0, 0, 0, 0)
        b2 = TradingClass.NewSingleOrder(2, 0, 0, 0, 0, 0, 0, 0, 180, 0, 220, 0, 0, 0, 0, 0)
        b3 = TradingClass.NewSingleOrder(3, 0, 0, 0, 0, 0, 0, 0, 100, 0, 190, 0, 0, 0, 0, 0)
        b4 = TradingClass.NewSingleOrder(4, 0, 0, 0, 0, 0, 0, 0, 50, 0, 180, 0, 0, 0, 0, 0)
        b5 = TradingClass.NewSingleOrder(5, 0, 0, 0, 0, 0, 0, 0, 560, 0, 210, 0, 0, 0, 0, 0)

        s6 = TradingClass.NewSingleOrder(6, 0, 0, 0, 0, 0, 0, 0, 90, 0, 230, 0, 0, 0, 0, 0)
        s7 = TradingClass.NewSingleOrder(7, 0, 0, 0, 0, 0, 0, 0, 230, 0, 230, 0, 0, 0, 0, 0)
        s8 = TradingClass.NewSingleOrder(8, 0, 0, 0, 0, 0, 0, 0, 40, 0, 180, 0, 0, 0, 0, 0)
        s9 = TradingClass.NewSingleOrder(9, 0, 0, 0, 0, 0, 0, 0, 600, 0, 170, 0, 0, 0, 0, 0)
        s10 = TradingClass.NewSingleOrder(10, 0, 0, 0, 0, 0, 0, 0, 140, 0, 200, 0, 0, 0, 0, 0)

        b = [b1, b2, b3, b4, b5]

        s = [s6, s7, s8, s9, s10]

        assert len(matching_algorithm.pro_rata([], [])) == 0
        assert len(matching_algorithm.pro_rata([], s)) == len(s)
        assert len(matching_algorithm.pro_rata(b, [])) == 0
        # TODO scenarios: 4,2 match perfectly, matched partially, only one 1 quantity
    """
    def test_extract_buy_and_sell_orders(self):
        dummy_orders = []
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.OrderSideType.SELL))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.OrderSideType.BUY))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.OrderSideType.SELL))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.OrderSideType.BUY))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.OrderSideType.SELL))
        buy_orders, sell_orders = matching_algorithm.extract_buy_and_sell_orders(dummy_orders)
        assert buy_orders[0] == dummy_orders[1]
        assert buy_orders[1] == dummy_orders[3]
        assert sell_orders[0] == dummy_orders[0]
        assert sell_orders[1] == dummy_orders[2]
        assert sell_orders[2] == dummy_orders[4]

    def test_determine_price_for_match_with_two_market_orders_and_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.OrderSideType.BUY,
                                                                 order_type=TradingClass.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.OrderSideType.SELL,
                                                                  order_type=TradingClass.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_two_market_orders_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.OrderSideType.BUY,
                                                                 order_type=TradingClass.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.OrderSideType.SELL,
                                                                  order_type=TradingClass.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.OrderSideType.BUY,
                                                                 order_type=TradingClass.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.OrderSideType.SELL,
                                                                 order_type=TradingClass.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.OrderSideType.BUY,
                                                                 order_type=TradingClass.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.OrderSideType.SELL,
                                                                 order_type=TradingClass.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 10. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_limit_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.OrderSideType.BUY,
                                                                order_type=TradingClass.OrderType.LIMIT)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.OrderSideType.SELL,
                                                                 order_type=TradingClass.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_limit_order, sell_limit_order)
        assert 9. == matched_price

    def test_create_order_execution_from_trading_matrix_entry(self):
        buy_market_order = TradingClass.Order.create_dummy_order(client_order_id="client",
                                                                 account_company_id="Client Firm", price=10.,
                                                                 received_date=TradingClass.FIXDate.from_fix_date_stamp_string(
                                                                     "20110805"), order_quantity=100.,
                                                                 side=TradingClass.OrderSideType.BUY,
                                                                 order_type=TradingClass.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(client_order_id="client",
                                                                  account_company_id="Client Firm", price=10.,
                                                                  received_date=TradingClass.FIXDate.from_fix_date_stamp_string(
                                                                      "20110804"), order_quantity=50.,
                                                                  side=TradingClass.OrderSideType.SELL,
                                                                  order_type=TradingClass.OrderType.MARKET)
        trading_matrix_entry = 55.5
        timestamp = TradingClass.FIXDateTimeUTC.from_date_fix_time_stamp_string("20111111-11:11:11")
        created_execution_order = matching_algorithm.create_order_execution_from_trading_matrix_entry(
            trading_matrix_entry=trading_matrix_entry,
            buy_order=buy_market_order,
            sell_order=sell_market_order,
            timestamp=timestamp)
        asserted_execution_order = TradingClass.OrderExecution(execution_id=None, quantity=trading_matrix_entry, price=10.,
                                                               execution_time=timestamp,
                                                               buyer_client_order_id=buy_market_order.client_order_id,
                                                               buyer_company_id=buy_market_order.account_company_id,
                                                               buyer_received_date=buy_market_order.received_date,
                                                               seller_client_order_id=sell_market_order.client_order_id,
                                                               seller_company_id=sell_market_order.account_company_id,
                                                               seller_received_date=sell_market_order.received_date)
        assert created_execution_order == asserted_execution_order

