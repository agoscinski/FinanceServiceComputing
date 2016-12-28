import server
import TradingClass

nasdaq_stock_ticker = "TESTTICKER"
nasdaq_stock = server.Stock(nasdaq_stock_ticker)

fsc_server_database_handler = server.ServerDatabaseHandler(user_name="root", user_password="root",
                                                           database_name="TestServerDatabase", database_port=3306,
                                                           init_database_script_path="./tests/database/server/init_test_server_database.sql")
server_application_id = "test"
fsc_server_logic = server.ServerLogic(server_application_id, server_database_handler=fsc_server_database_handler)

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


    def test_order_is_valid(self):
        # TODO Valentin
        pass


    def test_create_execution_report_for_order_execution(self):
        # TODO Emely
        dummy_order = TradingClass.OrderExecution.create_dummy_order_execution()
        fsc_server_logic.create_execution_report_for_order_execution(dummy_order)


    def test_create_execution_report_for_executed_order(self):
        # TODO Emely
        pass

    def test_check_if_order_cancel_is_valid(self):
        order = fsc_server_database_handler.fetch_latest_order_by_client_information('2', 'XX')
        valid = fsc_server_logic.check_if_order_cancel_is_valid(order)
        assert valid == False

        order = fsc_server_database_handler.fetch_latest_order_by_client_information('1', 'MS')
        valid = fsc_server_logic.check_if_order_cancel_is_valid(order)
        assert valid == False

        order = fsc_server_database_handler.fetch_latest_order_by_client_information('0', 'MS')
        valid = fsc_server_logic.check_if_order_cancel_is_valid(order)
        assert valid == True

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

    def test_fetch_pending_order_with_cumulative_quantity_by_stock_ticker(self):
        symbol = "TSLA"
        order_list = fsc_server_database_handler.fetch_pending_order_with_left_quantity_by_stock_ticker(symbol)
        goldman_sachs_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10000., price=1000.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 left_quantity=200.)
        morgan_stanley_order = TradingClass.Order(client_order_id='0', account_company_id='MS',
                                                  received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                      '2016-11-09'), handling_instruction=1,
                                                  maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                      '2016-11-20'), stock_ticker='TSLA',
                                                  side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                  order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                  order_quantity=2000., price=1010.,
                                                  last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                  left_quantity= 0.)
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

    def test_fetch_order_by_order_id(self):
        order_by_id = fsc_server_database_handler.fetch_order_by_order_id(0, 'GS', '2016-11-09')
        goldman_sachs_order = TradingClass.Order(client_order_id='0', account_company_id='GS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-15'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.BUY,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=10000., price=1000.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING,
                                                 left_quantity=None)
        assert order_by_id == goldman_sachs_order

    def test_insert_order_execution(self):
        order_execution = TradingClass.OrderExecution.create_dummy_order_execution(execution_id=None)
        order_id = fsc_server_database_handler.insert_order_execution(order_execution)
        assert order_id == 3

    def test_fetch_latest_order_by_client_information(self):
        db_order = fsc_server_database_handler.fetch_latest_order_by_client_information('0','MS')
        test_order = TradingClass.Order(client_order_id='0', account_company_id='MS',
                                                 received_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-09'), handling_instruction=1,
                                                 maturity_date=TradingClass.FIXDate.from_mysql_date_stamp_string(
                                                     '2016-11-20'), stock_ticker='TSLA',
                                                 side=TradingClass.DatabaseHandlerUtils.Side.SELL,
                                                 order_type=TradingClass.DatabaseHandlerUtils.OrderType.LIMIT,
                                                 order_quantity=2000., price=1010.,
                                                 last_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING)
        assert db_order == test_order
        pass

    def test_update_order_status(self):
        test_order=TradingClass.Order.create_dummy_order()
        test_order_status=TradingClass.DatabaseHandlerUtils.LastStatus.DONE
        assert fsc_server_database_handler.update_order_status(test_order,test_order_status) is not None
        db_order = fsc_server_database_handler.fetch_order_by_order_id(
            test_order.client_order_id,test_order.account_company_id,test_order.received_date)
        assert db_order.last_status == test_order_status

    def test_insert_order_cancel(self):
        test_requested_order_cancel=TradingClass.OrderCancel.create_dummy_order_cancel()
        assert fsc_server_database_handler.insert_order_cancel(test_requested_order_cancel) is not None

    def test_fetch_order_cancel(self):
        test_order_cancel=TradingClass.OrderCancel.create_dummy_order_cancel()
        fsc_server_database_handler.insert_order_cancel(test_order_cancel)
        db_order_cancel = fsc_server_database_handler.fetch_order_cancel(test_order_cancel.client_order_cancel_id)
        #Notes: side in database not retrieved, stock_ticker & order_quantity not in database not retrieved
        db_order_cancel.side = 2
        db_order_cancel.stock_ticker = "TSLA"
        db_order_cancel.order_quantity = 100
        #Executed time is generated when inserting database so it will not be the same to dummy created one
        test_order_cancel.execution_time = db_order_cancel.execution_time
        assert db_order_cancel == test_order_cancel
        pass

