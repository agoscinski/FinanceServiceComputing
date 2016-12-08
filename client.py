import sys
import quickfix as fix
import quickfix42 as fix42
import TradingClass
import datetime
import htmlPy
import json
import demjson

sys.path.append('GUI')
from frontEnd import htmlPy_app


class GUISignal(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    def __init__(self, gui_hadler):
        super(GUISignal, self).__init__()
        self.gui_handler = gui_hadler
        self.fresh = 1;
        # Initialize the class here, if required.
        return

    @htmlPy.Slot(str, str, result=str)
    def logIn(self, usr, psw):
        # login
        usr = str(usr)
        psw = str(psw)
        print usr, psw
        if (self.gui_handler.button_login_actuated(usr, psw)):
            return_message = '{"success":true,"userName":"' + usr + '"}'
        else:
            return_message = '{"success":false,"msg":"username or password is wrong"}'
        return return_message

    @htmlPy.Slot()
    def logOut(self):
        self.gui_handler.button_logout_actuated()

    @htmlPy.Slot(str)
    def searchStock(self, stockCode):
        self.gui_handler.search_for_stock_actuated(stockCode)

    @htmlPy.Slot(str)
    def refreshChart(self, market_data):
        # trading_transaction = TradingClass.TradingTransaction(["2016-10-01", "2016-10-02", "2016-10-03"], [12, 23, 12],
        #                                                       [22, 22, 22], [True, False, True])
        # stock_information = TradingClass.StockInformation(self.fresh, self.fresh + 2, self.fresh - 2)
        # stock_history = TradingClass.StockHistory(
        #     ["2016-10-1", "2016-10-2", "2016-10-3", "2016-10-4", "2016-10-5", "2016-10-6", "2016-10-7", "2016-10-8",
        #      "2016-10-9", "2016-10-10"],
        #     [self.fresh + 10, self.fresh + 12.5, 12.5, 12.5, self.fresh + 15.5, 12.5, 12.5, 12.5, 12.5, 12.5],
        #     [self.fresh, self.fresh, self.fresh, self.fresh, self.fresh, self.fresh, self.fresh, self.fresh, self.fresh,
        #      self.fresh])
        # order_book_buy = TradingClass.OrderBookBuy([11.5, 11.6, 11.7, 11.8, 11.9], [1, 2, 3, 4, 5])
        # order_book_sell = TradingClass.OrderBookSell([11.5, 11.6, 11.7, 11.8, 11.9], [1, 2, 3, 4, 5])
        # market_data = TradingClass.MarketData(stock_information, stock_history, order_book_buy, order_book_sell)


        quantity_chart_json = self.gui_handler.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.gui_handler.extract_course_chart_json(market_data)
        stock_information_json = self.gui_handler.extract_stock_information_json(market_data)
        order_book_json = self.gui_handler.extract_order_book_json(market_data)

        # trading_transaction_json = self.client_logic.gui_handler.extract_trading_transaction_json(trading_transaction)
        result = '{' + '"success":true' + ',"quantity":' + quantity_chart_json + ',"price":' + stock_course_chart_json + ',"stockInfo":' + stock_information_json + ',"orderBook":' + order_book_json + '}'
        htmlPy_app.evaluate_javascript("freshChart('" + result + "')")

    @htmlPy.Slot(str, str, str)
    def orderSell(self, price, quantity, type):
        print "sell:\n" + "price:" + price + "; quantity:" + quantity + "; type:" + type

    @htmlPy.Slot(str, str, str)
    def orderBuy(self, price, quantity, order_type):
        # TODO yelinsheng need stock_ticker string from one field
        # self.gui_handler.process_new_single_order_request(stock_ticker, TradingClass.FIXHandlerUtils.Side.BUY, order_type, price, quantity)
        pass

    @htmlPy.Slot(str, result=str)
    def get_form_data(self, json_data):
        # @htmlPy.Slot(arg1_type, arg2_type, ..., result=return_type)
        # This function can be used for GUI forms.
        #
        form_data = json.loads(json_data)
        print form_data
        print json.dumps(form_data)
        return json.dumps(form_data)

    @htmlPy.Slot()
    def javascript_function(self):
        # Any function decorated with @htmlPy.Slot decorater can be called
        # using javascript in GUI
        return


class ClientFIXApplication(fix.Application):
    order_id = 0
    market_data_request_id = 0

    def __init__(self, client_fix_handler):
        self.client_fix_handler = client_fix_handler
        super(ClientFIXApplication, self).__init__()

    def onCreate(self, session_id):
        print ("Application created - session: " + session_id.toString())
        self.sessionID = session_id

    def onLogon(self, session_id):
        print "Logon", session_id

    def onLogout(self, session_id):
        print "Logout", session_id

    def toAdmin(self, message, session_id):
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type.getString() == fix.MsgType_Logon:
            self.client_fix_handler.handle_to_be_sent_logon_request(message)

    def fromAdmin(self, message, session_id):
        pass

    def fromApp(self, message, session_id):
        print "IN", message
        msg_Type = message.getHeader().getField(fix.MsgType())
        if (msg_Type.getString() == fix.MsgType_MarketDataSnapshotFullRefresh):
            print "MarketDataSnapshotFullRefresh"
            self.client_fix_handler.handle_market_data_respond(message)
        elif (msg_Type.getString() == fix.MsgType_ExecutionReport):
            print "ExecutionReport"
            self.client_fix_handler.handle_execution_report(message)
        elif (msg_Type.getString() == fix.MsgType_OrderCancelReject):
            print "OrderCancelReject"
            self.client_fix_handler.handle_order_cancel_reject(message)

    def toApp(self, message, session_id):
        print "OUT", message

    def _calculate_checksum(self):
        pass

    def gen_order_id(self):
        self.order_id = self.order_id + 1
        return self.order_id

    def gen_market_data_request_id(self):
        self.market_data_request_id = self.market_data_request_id + 1
        return self.market_data_request_id


class ClientFIXHandler:
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
        self.client_database_handler = ClientDatabaseHandler(user_name="root", user_password="root",
                                                             database_name="BrokerDatabase", database_port=3306,
                                                             init_database_script_path="./database/init_client_database.sql")
        self.client_config_file_name = client_config_file_name
        self.fix_application = None
        self.socket_initiator = None
        self.storeFactory = None
        self.logFactory = None
        self.user_id = None
        self.password = None

    def init_fix_settings(self, default_client_config_file_name=None):
        client_config_file_name_ = self.client_config_file_name if default_client_config_file_name is None \
            else default_client_config_file_name
        settings = fix.SessionSettings(client_config_file_name_)
        self.fix_application = ClientFIXApplication(self)
        self.storeFactory = fix.FileStoreFactory(settings)
        self.logFactory = fix.FileLogFactory(settings)
        self.socket_initiator = fix.SocketInitiator(self.fix_application, self.storeFactory, settings, self.logFactory)

    def send_logon_request(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def connect_to_server(self):
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def handle_to_be_sent_logon_request(self, message):
        """Handle a logon request which is about to be sent

        Before the logon request is sent to the server, this function handles the message and modifies fields.

        Args:
            message (Swig Object of type 'FIX::Message *'): the message to be sent
        """
        pass

    def send_market_data_request(self, symbol):
        """Sends a market data request to server

        TODO @husein description if needed

        Args:
            symbol (string): the ticker symbol of a stock

        Returns:

        """
        # Create Fix Message for Market Data Request
        message = fix.Message();
        header = message.getHeader();
        header.setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        header.setField(fix.MsgSeqNum(self.client_database_handler.generate_new_client_order_id()))
        header.setField(fix.SendingTime())
        message.setField(fix.MDReqID(str(self.client_database_handler.generate_market_data_request_id())))
        message.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT))
        message.setField(fix.MarketDepth(1))
        message.setField(fix.NoMDEntryTypes(10))
        group_md_entry = fix42.MarketDataRequest().NoMDEntryTypes()
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_BID))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_OFFER))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_TRADE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_INDEX_VALUE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_OPENING_PRICE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_CLOSING_PRICE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_SETTLEMENT_PRICE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_TRADING_SESSION_HIGH_PRICE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_TRADING_SESSION_LOW_PRICE))
        message.addGroup(group_md_entry)
        group_md_entry.setField(fix.MDEntryType(fix.MDEntryType_TRADING_SESSION_VWAP_PRICE))
        message.addGroup(group_md_entry)

        group_symbol = fix42.MarketDataRequest().NoRelatedSym()
        group_symbol.setField(fix.Symbol(symbol))
        message.addGroup(group_symbol)

        # Send Fix Message to Server
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

        return

    def handle_market_data_respond(self, message):
        """Handles market data respond

        TODO @husein description if needed

        Args:
            message (FIX::Message): Market data message to be handled.

        Returns:
            TODO how does the return value look like
        """

        # Retrieve Market Data Response Type Full Refresh/Snapshot
        md_req_id_fix = fix.MDReqID()
        no_md_entries_fix = fix.NoMDEntries()
        symbol_fix = fix.Symbol()
        total_volume_traded_fix = fix.TotalVolumeTraded()
        md_entry_type_fix = fix.MDEntryType()
        md_entry_px_fix = fix.MDEntryPx()
        md_entry_size_fix = fix.MDEntrySize()
        md_entry_date_fix = fix.MDEntryDate()
        md_entry_time_fix = fix.MDEntryTime()
        md_entry_type_list = []
        md_entry_px_list = []
        md_entry_size_list = []
        md_entry_date_list = []
        md_entry_time_list = []

        message.getField(md_req_id_fix)
        message.getField(no_md_entries_fix)
        message.getField(symbol_fix)
        message.getField(total_volume_traded_fix)

        a_date = TradingClass.FIXDate.from_year_month_day(2000, 1, 1)
        a_time = TradingClass.FIXTime(0, 0, 0)
        groupMD = fix42.MarketDataSnapshotFullRefresh.NoMDEntries()
        for MDIndex in range(no_md_entries_fix.getValue()):
            message.getGroup(MDIndex + 1, groupMD)
            groupMD.getField(md_entry_type_fix)
            groupMD.getField(md_entry_px_fix)
            groupMD.getField(md_entry_size_fix)
            groupMD.getField(md_entry_date_fix)
            groupMD.getField(md_entry_time_fix)
            a_date.set_date_from_date_stamp_string(md_entry_date_fix.getString())
            a_time.set_time_string(md_entry_time_fix.getString())
            md_entry_type_list.append(md_entry_type_fix.getValue())
            md_entry_px_list.append(md_entry_px_fix.getValue())
            md_entry_size_list.append(md_entry_size_fix.getValue())
            md_entry_date_list.append(a_date)
            md_entry_time_list.append(a_time)

        # Encapsulate data into market data response object
        market_data = TradingClass.MarketDataResponse(md_req_id_fix.getValue(), no_md_entries_fix.getValue(),
                                                      symbol_fix.getValue()
                                                      , md_entry_type_list, md_entry_px_list, md_entry_size_list,
                                                      md_entry_date_list,
                                                      md_entry_time_list, total_volume_traded_fix.getValue())

        self.client_logic.process_market_data_respond(market_data)
        pass

    def send_order_cancel_request(self, order_cancel_request):
        # Create Fix Message for Order Cancel Request
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))
        transact_time_fix = fix.TransactTime()
        transact_time_fix.setString(order_cancel_request.transact_time.__str__())

        message.setField(fix.OrigClOrdID(order_cancel_request.orig_cl_ord_id))
        message.setField(fix.ClOrdID(order_cancel_request.cl_ord_id))
        message.setField(fix.Symbol(order_cancel_request.symbol))
        message.setField(fix.Side(order_cancel_request.side))
        message.setField(transact_time_fix)
        message.setField(fix.OrderQty(order_cancel_request.order_qty))

        # Send Fix Message to Server
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

    def handle_order_cancel_reject(self, message):
        order_cancel_reject = TradingClass.OrderCancelReject.from_fix_message(message)
        self.client_logic.process_order_cancel_reject(order_cancel_reject)

    def send_new_single_order(self, new_single_order):
        """Sends an new single order to server

        Args:
            new_single_order (TradingClass.NewSingleOrder):

        Returns:
            None
        """
        message = new_single_order.to_fix_message()
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

        return

    def handle_execution_report(self, message):
        order_id = self.get_field_value(fix.OrderID(), message)
        cl_ord_id = self.get_field_value(fix.ClOrdID(), message)
        orig_cl_ord_id = self.get_field_value(fix.OrigClOrdID(), message)
        exec_id = self.get_field_value(fix.ExecID(), message)
        exec_trans_type = self.get_field_value(fix.ExecTransType(), message)
        exec_type = self.get_field_value(fix.ExecType(), message)
        ord_status = self.get_field_value(fix.OrdStatus(), message)
        symbol = self.get_field_value(fix.Symbol(), message)
        side = self.get_field_value(fix.Side(), message)
        leaves_qty = self.get_field_value(fix.LeavesQty(), message)
        cum_qty = self.get_field_value(fix.CumQty(), message)
        avg_px = self.get_field_value(fix.AvgPx(), message)
        price = self.get_field_value(fix.Price(), message)
        stop_px = self.get_field_value(fix.StopPx(), message)

        # Encapsulate result of receiving execution report into order execution report
        if ord_status == '4':
            self.client_logic.process_order_cancel_respond(orig_cl_ord_id, ord_status, leaves_qty, cum_qty)
        else:
            order_execution = TradingClass.OrderExecution(order_id, cl_ord_id, exec_id, exec_trans_type, exec_type,
                                                          ord_status, symbol
                                                          , side, leaves_qty, cum_qty, avg_px, price, stop_px)
            self.client_logic.process_order_execution_respond(order_execution)

        return

    def send_logout_request(self):
        self.socket_initiator.stop()

    def get_field_value(self, fix_object, message):
        if message.isSetField(fix_object.getField()):
            message.getField(fix_object)
            return fix_object.getValue()
        else:
            return None

    def get_field_string(self, fix_object, message):
        if message.isSetField(fix_object.getField()):
            message.getField(fix_object)
            return fix_object.getString()
        else:
            return None

    def get_header_field_value(self, fix_object, message):
        if message.getHeader().isSetField(fix_object.getField()):
            message.getHeader().getField(fix_object)
            return fix_object.getValue()
        else:
            return None

    def get_header_field_string(self, fix_object, message):
        if message.getHeader().isSetField(fix_object.getField()):
            message.getHeader().getField(fix_object)
            return fix_object.getString()
        else:
            return None


class ClientLogic():
    def __init__(self, client_config_file_name):
        self.client_fix_handler = ClientFIXHandler(self, client_config_file_name)
        self.client_database_handler = ClientDatabaseHandler()
        self.gui_handler = GUIHandler(self)
        self.gui_signal = GUISignal(self.gui_handler)

    def start_client(self):
        # start some gui stuff and other things, for now only gui
        self.gui_handler.start_gui()

    def logon(self):
        self.client_fix_handler.connect_to_server()

        # TODO block mechanism
        self.block_gui()
        return

    def block_gui(self):
        pass

    def logout(self):
        self.client_fix_handler.send_logout_request()

    def process_market_data_request(self, symbol):
        self.client_fix_handler.send_market_data_request(symbol)

    def process_market_data_respond(self, market_data):
        """Process market data respond

        Args:
            market_data object of MarketDataResponse .

        Returns:
            None
        """
        # Example of printing market_data response object
        print "fresh chart"
        print market_data.no_md_entry_types
        print market_data.symbol
        for j in range(market_data.no_md_entry_types):
            print(market_data.md_entry_type_list[j])
            print(market_data.md_entry_px_list[j])
            print(market_data.md_entry_size_list[j])
            print(market_data.md_entry_date_list[j])
            print(market_data.md_entry_time_list[j])

        offers_price, offers_quantity, bids_price, bid_quantity, current_price, current_quantity, opening_price, \
        closing_price, day_high, day_low = self.extract_market_data_information(market_data)
        # TODO tobefixed not working comment it out to avoid error
        """
        five_smallest_offers_price, five_smallest_offers_quantity = self.extract_five_smallest_offers(offers_price,
                                                                                                      offers_quantity)
        five_biggest_bids_price, five_biggest_bids_quantity = self.extract_five_biggest_bids(bids_price, bid_quantity)
        """
        print offers_price, offers_quantity, bids_price, bid_quantity, current_price, current_quantity, opening_price, closing_price, day_high, day_low
        # TODO here should be some database interaction

        # TODO tobefixed not working comment it out to avoid error
        """
        order_book_buy = TradingClass.OrderBookBuy(five_biggest_bids_price, five_biggest_bids_quantity)
        order_book_sell = TradingClass.OrderBookBuy(five_smallest_offers_price, five_smallest_offers_quantity)
        """
        order_book_buy = TradingClass.OrderBookBuy([100, 200, 300, 400, 500], [10, 20, 30, 40, 50])
        order_book_sell = TradingClass.OrderBookBuy([100, 90, 80, 70, 60], [10, 11, 12, 13, 15, 16])
        stock_information = TradingClass.StockInformation(current_price, day_high, day_low)

        # TODO how todo date
        current_date = datetime.date.today()
        stock_history = TradingClass.StockHistory(current_date, current_price, current_quantity)
        gui_market_data = TradingClass.MarketData(stock_information, stock_history, order_book_buy, order_book_sell)

        self.gui_handler.refresh_charts(gui_market_data)

        return

    def process_new_single_order_request(self, stock_ticker, side, order_type, price, quantity):
        """This function processes and order and sends it to the server
        Args:
            stock_ticker (string)
            side (int/FIXHandler.Side)
            order_type (char/FIXHandler.OrderType)
            price (float)
            quantity (float)
        """
        client_order_id = self.client_database_handler.generate_new_client_order_id()
        maturity_month_year, maturity_day = self.get_tomorrows_maturity_date()
        handling_instruction = TradingClass.FIXHandlerUtils.HandlingInstruction.AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION
        sending_time = TradingClass.FIXDateTimeUTC.create_for_current_time()
        new_single_order = TradingClass.NewSingleOrder(client_order_id=client_order_id, symbol=stock_ticker, side=side,
                                                       price=price, order_quantity=quantity,
                                                       transaction_time=sending_time, order_type=order_type,
                                                       handling_instruction=handling_instruction,
                                                       maturity_month_year=maturity_month_year,
                                                       maturity_day=maturity_day)
        client_order = TradingClass.ClientOrder.from_new_single_order(new_single_order,
                                                                      last_status=TradingClass.DatabaseHandlerUtils.LastStatus.NOT_YET_ACKNOWLEDGED,
                                                                      average_price=0, quantity_filled=0)
        self.client_database_handler.insert_order(client_order)
        self.client_fix_handler.send_new_single_order(new_single_order)
        return

    def process_order_execution_respond(self, order_execution):
        # process execution respond from server

        if order_execution.ord_status == '0':
            print("Receive ACK")
        elif order_execution.ord_status == '1':
            print("Order Status Partially Filled")
        elif order_execution.ord_status == '2':
            print("Order Status Filled")
        elif order_execution.ord_status == '4':
            print("Cancel Order Success")
        elif order_execution.ord_status == '5':
            print("Replace Order Success")
        elif order_execution.ord_status == '8':
            print("Do Rejected Order")

        print("exec_id_fix, exec_trans_type_fix,exec_type_fix,ord_status_fix,symbol_fix,side_fix,eaves_qty_fix,"
              "cum_qty_fix,avg_px_fix,price_fix,stop_px_fix,")
        print(order_execution.order_id)
        print(order_execution.exec_id)
        print(order_execution.exec_trans_type)
        print(order_execution.exec_type)
        print(order_execution.ord_status)
        print(order_execution.symbol)
        print(order_execution.side)
        print(order_execution.leaves_qty)
        print(order_execution.cum_qty)
        print(order_execution.avg_px)
        print(order_execution.price)
        print(order_execution.stop_px)
        return

    def process_order_cancel_request(self, order_id):
        # Construct Fix Order Object to be sent to the fix handler
        orig_cl_ord_id = order_id
        cl_ord_id = '1'  # self.client_fix_handler.fix_application.gen_order_id()
        # should be retrieved from database
        symbol = 'TSLA'
        side = TradingClass.FIXHandlerUtils.Side.BUY
        order_qty = 100
        transact_time = TradingClass.FIXDateTimeUTC.create_for_current_time()
        ocr = TradingClass.OrderCancelRequest(orig_cl_ord_id, cl_ord_id, symbol, side, transact_time, order_qty)
        self.client_fix_handler.send_order_cancel_request(ocr)
        return

    def process_order_cancel_respond(self, order_cl_ord_id, ord_status, leaves_qty, cum_qty):
        # TODO Database Query Update Order Status in client database
        print "process order cancel respond"

    def process_order_cancel_reject(self, order_cancel_reject):
        # TODO Database Query Update Order Cancel Rejected
        print "reject the order cancellation"

    def request_trading_transactions(self, user_name):
        # TODO alex write database request/fetch
        # TODO FIRST yelinsheng sample data
        trading_transaction = None
        return trading_transaction

    def get_tomorrows_maturity_date(self):
        """Returns the standard maturity date which is the date of tomorrow
        Returns:
            maturity_date (FIXYearMonth)
            maturity_day (int): between 1-31
        """
        # TODO Valentin
        maturity_date = TradingClass.FIXYearMonth.from_date_stamp_string("201612")
        maturity_day = 1
        return maturity_date, maturity_day


class ClientDatabaseHandler(TradingClass.DatabaseHandler):
    last_order_id = 0
    last_market_data_request_id = 0

    def insert_order(self, order):
        """Insert a order into the the client database
        Args:
            order (TradingClass.Order)
        Returns:
            None
        """
        # TODO Valentin use execute_nonresponsive_sql_command for this
        pass

    def generate_new_client_order_id(self):
        # TODO Alex when the cfg is implemented add account name id into client order id
        TradingClass.FIXDateTimeUTC.create_for_current_time()
        return "client_" + str(datetime.datetime.utcnow())

    def insert_order(self, order):
        """Inserts an order into client database
        Args:
            order (TradingClass.ClientOrder): order to be inserted

        Return:
            None
        """
        command = (
            "INSERT INTO `Order`(OrderID, TransactionTime, Side, OrderType, OrderQuantity, OrderPrice, LastStatus, "
            "MaturityDate, QuantityFilled, AveragePrice) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            % (order.order_id, order.transaction_time.mysql_date_stamp_string, str(order.side), str(order.order_type),
               str(order.order_quantity), str(order.order_price), str(order.last_status), order.maturity_day.mysql_date_stamp_string,
               str(order.quantity_filled), str(order.average_price)))
        self.execute_nonresponsive_sql_command(command)
        return

    def generate_market_data_request_id(self):
        self.last_market_data_request_id = self.last_market_data_request_id + 1
        return self.last_market_data_request_id


class GUIHandler:
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        while (True):
            print '''input 1 to run in terminal\ninput 2 to start gui\ninput 3 to quit'''
            input = raw_input()
            # input='2'
            if (input == '1'):
                self.wait_for_input()
            elif (input == '2'):
                json = {
                }
                htmlPy_app.template = ("index.html", json)
                htmlPy_app.bind(self.client_logic.gui_signal)
                htmlPy_app.start()
            elif (input == '3'):
                break
            else:
                continue

    def wait_for_input(self):
        while True:
            print '''input 1 to logon\ninput 2 to logout\ninput 3 to send market request\ninput 4 to order\ninput 5 to cancel order\n input 6 to quit'''
            input = raw_input()
            if input == '1':
                self.button_login_actuated("john", "papapa")
            elif input == '2':
                self.button_logout_actuated()
            elif input == '3':
                self.send_market_data_request_option("TSLA")
            elif input == '4':
                self.send_dummy_order()
            elif input == '5':
                self.send_order_cancel_request_option("1")
            elif input == '6':
                break
            else:
                continue

    def button_login_actuated(self, user_name, user_password):
        """This function is activated when the login button is pushed"""
        return self.client_logic.logon()

    def request_trading_transactions(self, user_name):
        """Request trading transactions

        Args:
            user_name (string): .

        Returns:
        trading_transactions (string): json string of trading transaction
        """
        trading_transactions = self.client_logic.request_trading_transactions(user_name)
        # TODO yenlinsheng finish this function
        trading_transactions_json = self.extract_trading_transactions_json(trading_transactions)
        pass

    def button_logout_actuated(self):
        """This function is activated when the login button is pushed"""
        respond = self.client_logic.logout()

    def send_market_data_request_option(self, symbol):
        self.client_logic.process_market_data_request(symbol)

    # this function is used for button_buy_actuated as long it does not work
    def send_dummy_order(self):
        """For testing"""
        dummy_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        self.button_buy_actuated(dummy_order.symbol, dummy_order.side, dummy_order.order_type, dummy_order.price,
                                 dummy_order.order_quantity)

    def send_order_cancel_request_option(self, order_id):
        self.client_logic.process_order_cancel_request(order_id)

    def button_buy_actuated(self, stock_ticker, side, order_type, price, quantity):
        """
        Args:
            stock_ticker (string)
            side (int/FIXHandlerUtils.Side)
            order_type (int/FIXHandlerUtils.OrderType)
            price (float)
            quantity (float)
        """
        self.client_logic.process_new_single_order_request(stock_ticker, side, order_type, price, quantity)
        # TODO alex
        pass

    def button_sell_actuated(self, stock_ticker, price, quantity):
        # TODO alex
        pass

    def search_for_stock_actuated(self, searching_value):
        """This function is called when the user enters a search request

        Args:
            searching_value (string): The value of the user input

        Returns:
            None
        """
        stock_ticker_symbol = str(searching_value)
        print "Request market data for " + stock_ticker_symbol
        self.client_logic.process_market_data_request(stock_ticker_symbol)

    def refresh_charts(self, market_data):
        """This function

        Args
            market_data TradingClass.MarketData
        :return:
        """
        print "fresh chart"

        '''
        # TODO yenlinsheng finish these functions
        quantity_chart_json = self.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.extract_course_chart_json(market_data)
        stock_information_json = self.extract_stock_information_json(market_data)
        order_book_json = self.extract_order_book_json(market_data)
        return quantity_chart_json, stock_course_chart_json, stock_information_json, order_book_json
        '''
        self.client_logic.gui_signal.refreshChart(market_data)

    def refresh_trading_transaction_list(self, trading_transaction):
        # TODO yenlinsheng finish this function
        trading_transaction_json = self.extract_trading_transaction_json(trading_transaction)
        return trading_transaction_json

    def extract_quantity_chart_json(self, market_data):
        data = {"content": []}
        for i in range(len(market_data.stock_history.time)):
            tmp = {}
            tmp["time"] = market_data.stock_history.time[i]
            tmp["quantity"] = market_data.stock_history.quantity[i]
            data["content"].append(tmp)
        return demjson.encode(data)

    def extract_course_chart_json(self, market_data):
        data = {"content": []}
        for i in range(len(market_data.stock_history.time)):
            tmp = {}
            tmp["time"] = market_data.stock_history.time[i]
            tmp["price"] = market_data.stock_history.price[i]
            data["content"].append(tmp)
        return demjson.encode(data)

    def extract_stock_information_json(self, market_data):
        data = {}
        data["price"] = market_data.stock_information.price
        data["high"] = market_data.stock_information.high
        data["low"] = market_data.stock_information.low
        return demjson.encode(data)

    def extract_order_book_json(self, market_data):
        data = {"buy": [], "sell": []}
        for i in range(len(market_data.order_book_buy.price)):
            tmp = {}
            tmp["price"] = market_data.order_book_buy.price[i]
            tmp["quantity"] = market_data.order_book_buy.quantity[i]
            data["buy"].append(tmp)
        for i in range(len(market_data.order_book_sell.price)):
            tmp = {}
            tmp["price"] = market_data.order_book_sell.price[i]
            tmp["quantity"] = market_data.order_book_sell.quantity[i]
            data["sell"].append(tmp)
        return demjson.encode(data)

    def extract_trading_transaction_json(self, trading_transaction):
        data = {"content": []}
        for i in range(len(trading_transaction.time)):
            tmp = {}
            tmp["time"] = trading_transaction.time[i]
            tmp["price"] = trading_transaction.price[i]
            tmp["quantity"] = trading_transaction.quantity[i]
            tmp["side"] = ("buy" if trading_transaction.side[i] else "sell")
            data["content"].append(tmp)
        return demjson.encode(data)
