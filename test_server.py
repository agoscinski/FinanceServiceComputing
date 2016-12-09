import server
import TradingClass

nasdaq_stock_ticker = "TESTTICKER"
nasdaq_stock = server.Stock(nasdaq_stock_ticker)

fsc_server_database_handler = server.ServerDatabaseHandler(user_name="root", user_password="root",
                                                           database_name="TestFSCDatabase", database_port=3306,
                                                           init_database_script_path="./tests/database/init_test_database.sql")
server_config_file_name = "server.cfg"
fsc_server_logic = server.ServerLogic(server_config_file_name, fsc_server_database_handler)


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    fsc_server_database_handler.init_database()


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    fsc_server_database_handler.teardown_database()


class TestServerLogic:
    def test_create_execution_report_for_new_order(self):
        dummy_order = TradingClass.Order.create_dummy_order()
        fsc_server_logic.create_execution_report_for_new_order(dummy_order)


class TestServerDatabaseHandler:

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        fsc_server_database_handler.init_database()

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        fsc_server_database_handler.teardown_database()

    def test_check_if_order_is_valid(self):


        good_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10., price=550.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 cumulative_order_quantity=10.)
        assert Server.check_if_order_is_valid(too_expensive_order) == True

        #Accept orders with price in proper range, which means 10% away from last price.  Reject the rest orders with reason.
          too_expensive_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10., price=606.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 cumulative_order_quantity=10.)
          assert Server.check_if_order_is_valid(too_expensive_order) == False

          too_cheap_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10., price=494.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 cumulative_order_quantity=10.)
          assert Server.check_if_order_is_valid(too_cheap_order) == False

        #Accept orders with notional value in proper range, which means within 20% of total tradable value of the target stock.
          too_big_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=34., price=500.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 cumulative_order_quantity=34.)
          assert Server.check_if_order_is_valid(too_big_order) == False
          
        #Accept orders during auction, normal trading session.  Reject orders after close, before open.
          too_late_order = TradingClass.Order(cls, client_order_id="client", 
                                                  handling_instruction="1",
                                                  symbol="TSLA", 
                                                  maturity_month_year=FIXYearMonth.from_year_month(2016, 12),
                                                  maturity_day=2, 
                                                  side=FIXHandlerUtils.Side.BUY,
                                                  transaction_time=FIXDateTimeUTC.from_date_fix_time_stamp_string("20161212-00:00:00"),
                                                  order_quantity=10., 
                                                  order_type=FIXHandlerUtils.OrderType.LIMIT, 
                                                  price=500.,
                                                  stop_price=None, 
                                                  sender_company_id=None, 
                                                  sending_time=None,
                                                  on_behalf_of_company_id=None, 
                                                  sender_sub_id=None)
          assert Server.check_if_order_is_valid(too_late_order) == False
        #TODO Valentin

    def test_create_execution_report_for_order_execution(self):
        #TODO Emely
        pass

    def test_create_execution_report_for_executed_order(self):
        #TODO Emely
        pass

    def test_fetch_pending_order_with_cumulative_quantity_by_stock_ticker(self):
        symbol = "TSLA"
        order_list = fsc_server_database_handler.fetch_pending_order_with_cumulative_quantity_by_stock_ticker(symbol)
        goldman_sachs_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10000., price=1000.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 cumulative_order_quantity=200.)
        morgan_stanley_order = TradingClass.Order(client_order_id='0', account_company_id='MS',
                                                  received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                      '2016-11-09'), handling_instruction=1,
                                                  maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                      '2016-11-20'), stock_ticker='TSLA',
                                                  side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                  order_quantity=2000., price=1010.,
                                                  last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                  cumulative_order_quantity = 0.)
        assert order_list.__contains__(goldman_sachs_order)
        assert order_list.__contains__(morgan_stanley_order)

    def test_fetch_cumulative_quantity_and_average_price_by_order_id(self):
        client_order_id, account_company_id, received_date = '0', 'GS', TradingClass.FIXDate.from_mysql_date_stamp_string(
            '2016-11-09')
        cumulative_quantity, average_price = fsc_server_database_handler.fetch_cumulative_quantity_and_average_price_by_order_id(
            client_order_id, account_company_id, received_date)
        asserted_cumulative_quantity = float(100 + 100)
        asserted_average_price = (1100 + 550) / 2.
        assert asserted_cumulative_quantity == cumulative_quantity
        assert asserted_average_price == average_price

    # do inserts here so they do not interfere with logical tests
    def test_execute_responsive_insert_sql_command(self):
        insert_sql = "INSERT INTO OrderExecution(OrderExecutionQuantity, OrderExecutionPrice, ExecutionTime," \
                     " Order_BuyClientOrderID, Order_BuyCompanyID, Order_BuyReceivedDate, Order_SellClientOrderID," \
                     " Order_SellCompanyID, Order_SellReceivedDate) VALUES('100','550','2016-11-09 12:14:07', '0','GS'," \
                     "'2016-11-09', '1','MS','2016-11-08')"
        execution_id = fsc_server_database_handler.execute_responsive_insert_sql_command(insert_sql)
        assert execution_id == 3

    def test_insert_order(self):
        dummy_order = TradingClass.Order.create_dummy_order(msg_seq_num=0)
        fsc_server_database_handler.insert_order(dummy_order)
    """
    def test_fetch_order_by_order_id(self):
        order = fsc_server_database_handler.fetch_order_by_order_id(0, 'GS', '2016-11-09')
        assert order_id == 1 #TODO fetch_order_by_order_id returns an TradingClass.Order object so you need to compare these two kinds

    """

    def test_insert_order_execution(self):
        order_execution = TradingClass.OrderExecution.create_dummy_order_execution(execution_id=None)
        assert fsc_server_database_handler.insert_order_execution(order_execution) == 3
