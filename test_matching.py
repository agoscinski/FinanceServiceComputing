import TradingClass
import matching_algorithm
import copy

class TestMatchingAlgorithm:

    def test_pro_rata(self):
        buy_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=120, price=200)
        sell_order = TradingClass.Order.create_dummy_order(cumulative_order_quantity=120, price=200)

        buy_orders = [copy.copy(buy_order), copy.copy(buy_order), copy.copy(buy_order), copy.copy(buy_order), copy.copy(buy_order)]
        sell_orders = [copy.copy(sell_order), copy.copy(sell_order), copy.copy(sell_order), copy.copy(sell_order), copy.copy(sell_order)]

        assert matching_algorithm.pro_rata([], []) is None
        assert matching_algorithm.pro_rata([], sell_orders) is None
        assert matching_algorithm.pro_rata(buy_orders, []) is None
        # shape test
        result_matrix = matching_algorithm.pro_rata(buy_orders, sell_orders)
        assert result_matrix.shape == (len(sell_orders), len(buy_orders))

    def test_volume_pro_rata(self):

        b1 = TradingClass.Order(1, 0, 0, 0, 0, 0, 0, 0, 120, 200, 0)
        b2 = TradingClass.Order(2, 0, 0, 0, 0, 0, 0, 0, 180, 220, 0)
        b3 = TradingClass.Order(3, 0, 0, 0, 0, 0, 0, 0, 100, 190, 0)
        b4 = TradingClass.Order(4, 0, 0, 0, 0, 0, 0, 0, 50, 180, 0)
        b5 = TradingClass.Order(5, 0, 0, 0, 0, 0, 0, 0, 560, 210, 0)

        s6 = TradingClass.Order(6, 0, 0, 0, 0, 0, 0, 0, 90, 230, 0)
        s7 = TradingClass.Order(7, 0, 0, 0, 0, 0, 0, 0, 230, 230, 0)
        s8 = TradingClass.Order(8, 0, 0, 0, 0, 0, 0, 0, 40, 180, 0)
        s9 = TradingClass.Order(9, 0, 0, 0, 0, 0, 0, 0, 600, 170, 0)
        s10 = TradingClass.Order(10, 0, 0, 0, 0, 0, 0, 0, 140, 200, 0)

        b = [b1, b2, b3, b4, b5]

        s = [s6, s7, s8, s9, s10]

        volume_of_buy = 0
        volume_of_sell = 0

        for i in range(len(b)):
            volume_of_buy += b[i].cumulative_order_quantity

        for i in range(len(s)):
            volume_of_sell += s[i].cumulative_order_quantity

        assert (volume_of_buy == 1010)
        assert (volume_of_sell == 1100)

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
        buy_market_order = TradingClass.Order.create_dummy_order(price=10.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=8.,
                                                                  side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_two_market_orders_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_market_order = TradingClass.Order.create_dummy_order(price=10.,
                                                                  side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_market_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=10.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 9. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_no_intersection(self):
        buy_market_order = TradingClass.Order.create_dummy_order(price=8.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.MARKET)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=10.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        matched_price = matching_algorithm.determine_price_for_match(buy_market_order, sell_limit_order)
        assert 10. == matched_price

    def test_determine_price_for_match_with_one_market_one_limit_order_and_intersection(self):
        buy_limit_order = TradingClass.Order.create_dummy_order(price=10.,
                                                                side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                                order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT)
        sell_limit_order = TradingClass.Order.create_dummy_order(price=8.,
                                                                 side=TradingClass.DatabaseHandlerUtils.Side.SELL,
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
        asserted_execution_order = TradingClass.OrderExecution(execution_id=None, quantity=trading_matrix_entry,
                                                               price=10.,
                                                               execution_time=timestamp,
                                                               buyer_client_order_id=buy_market_order.client_order_id,
                                                               buyer_company_id=buy_market_order.account_company_id,
                                                               buyer_received_date=buy_market_order.received_date,
                                                               seller_client_order_id=sell_market_order.client_order_id,
                                                               seller_company_id=sell_market_order.account_company_id,
                                                               seller_received_date=sell_market_order.received_date)
        assert created_execution_order == asserted_execution_order
