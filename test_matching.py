import TradingClass
import matching_algorithm


class TestMatchingAlgorithm:

    def test_pro_rata(self):
        buy_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=120, price=200)
        sell_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=120, price=200)

        buy_orders = [buy_order, buy_order, buy_order, buy_order, buy_order]
        sell_orders = [sell_order, sell_order, sell_order, sell_order, sell_order]

        assert matching_algorithm.pro_rata([], []) is None
        assert matching_algorithm.pro_rata([], sell_orders) is None
        assert matching_algorithm.pro_rata(buy_orders, []) is None
        # shape test
        assert  matching_algorithm.pro_rata(buy_orders, sell_orders).shape == (len(sell_orders), len(buy_orders))

    def test_extract_buy_and_sell_orders(self):
        dummy_orders = []
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.DatabaseHandlerUtils.Side.SELL))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.DatabaseHandlerUtils.Side.BUY))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.DatabaseHandlerUtils.Side.SELL))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.DatabaseHandlerUtils.Side.BUY))
        dummy_orders.append(TradingClass.Order.create_dummy_order(side=TradingClass.DatabaseHandlerUtils.Side.SELL))
        buy_orders, sell_orders = matching_algorithm.extract_buy_and_sell_orders(dummy_orders)
        assert buy_orders[0] == dummy_orders[1]
        assert buy_orders[1] == dummy_orders[3]
        assert sell_orders[0] == dummy_orders[0]
        assert sell_orders[1] == dummy_orders[2]
        assert sell_orders[2] == dummy_orders[4]

    def test_determine_price_for_match_with_two_market_orders_and_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_two_market_orders_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 10. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_limit_order = TradingClass.Order.create_dummy_order(price=10., side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8., side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_limit_order, sell_limit_order)
        assert 9. == matched_price

    def test_create_order_execution_from_trading_matrix_entry(self):
        buy_market_order = TradingClass.Order.create_dummy_order(client_order_id="client",
                                                                 account_company_id="Client Firm", price=10.,
                                                                 received_date=TradingClass.FIXDate.from_fix_date_stamp_string(
                                                                     "20110805"), order_quantity=100.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(client_order_id="client",
                                                                  account_company_id="Client Firm", price=10.,
                                                                  received_date=TradingClass.FIXDate.from_fix_date_stamp_string(
                                                                      "20110804"), order_quantity=50.,
                                                                  side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
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

