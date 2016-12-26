import sys
import quickfix as fix
import quickfix42 as fix42
import TradingClass
import utils
import datetime
import htmlPy
import json
import demjson

sys.path.append('GUI')
from frontEnd import htmlPy_app


class GUISignal(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    def __init__(self, gui_handler):
        super(GUISignal, self).__init__()
        self.gui_handler = gui_handler
        self.fresh = 1;
        # Initialize the class here, if required.
        return

    @htmlPy.Slot()
    def logIn(self):
        self.gui_handler.button_login_actuated()

    @htmlPy.Slot()
    def logOut(self):
        self.gui_handler.client_logic.logout()
        transactionJson='{"content":[]}'
        self.refreshTransaction(transactionJson)

    @htmlPy.Slot(str)
    def searchStock(self, stockCode):
        self.gui_handler.search_for_stock_actuated(stockCode)

    @htmlPy.Slot(str)
    def orderCancel(self, OrderID):
        self.gui_handler.button_cancel_actuated(OrderID)

    @htmlPy.Slot(str)
    def refreshTransaction(self,transactionJson):
        """This function is called to refresh transaction area in GUI
        Args:
            client transaction json can be fetched as follow:
            transactionJson = self.gui_handler.request_trading_transactions()
        """
        htmlPy_app.evaluate_javascript('refreshTransaction(\'' + transactionJson + '\')')

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

    @htmlPy.Slot(str, str, str, str)
    def orderSell(self, price, quantity, order_type, ticket_code):
        if order_type == 'limit':
            order_type = TradingClass.FIXHandlerUtils.OrderType.LIMIT
        elif order_type == 'market':
            order_type = TradingClass.FIXHandlerUtils.OrderType.MARKET
        self.gui_handler.client_logic.process_new_single_order_request(stock_ticker=str(ticket_code),
                                                                       side=TradingClass.FIXHandlerUtils.Side.SELL,
                                                                       order_type=order_type, price=float(price),
                                                                       quantity=float(quantity))

    @htmlPy.Slot(str, str, str, str)
    def orderBuy(self, price, quantity, order_type, ticket_code):
        if order_type == 'limit':
            order_type = TradingClass.FIXHandlerUtils.OrderType.LIMIT
        elif order_type == 'market':
            order_type = TradingClass.FIXHandlerUtils.OrderType.MARKET
        self.gui_handler.client_logic.process_new_single_order_request(stock_ticker=str(ticket_code),
                                                                       side=TradingClass.FIXHandlerUtils.Side.BUY,
                                                                       order_type=order_type, price=float(price),
                                                                       quantity=float(quantity))

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
    def __init__(self, client_logic, client_database_handler):
        self.client_logic = client_logic
        self.client_database_handler = client_database_handler
        self.client_config_file_name = utils.ClientConfigFileHandler(
            application_id=self.client_logic.application_id, start_time=str(self.client_logic.start_time),
            end_time=str(self.client_logic.end_time),
            file_store_path="storage/client_" + self.client_logic.application_id + "_messages",
            file_log_path="log/client_" + self.client_logic.application_id + "_messages",
            socket_accept_port="5502", socket_connect_port="5501", target_comp_id="main_server").create_config_file()
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

    def connect_to_server(self):
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def handle_to_be_sent_logon_request(self, message):
        """Handle a logon request which is about to be sent

        Before the logon request is sent to the server, this function handles the message and modifies fields.

        Args:
            message (Swig Object of type 'FIX::Message *'): the message to be sent

        Returns:
            None
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
        """
        Args:
            order_cancel_request (TradingClass.OrderCancelRequest)
        Returns:
            None
        """
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
        print("avg_px, cum_qty")
        print(avg_px, cum_qty)

        order_execution = TradingClass.ExecutionReport(order_id, cl_ord_id, exec_id, exec_trans_type, exec_type,
                                                       ord_status, symbol, side, leaves_qty, cum_qty, avg_px, price, orig_cl_ord_id)
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
    """
    Attributes:
        application_id (string)
        start_time (datetime.time)
        end_time (datetime.time)
        client_fix_handler (

    """

    def __init__(self, application_id):
        self.client_database_handler = ClientDatabaseHandler(database_host="localhost",
                                                             user_name="root", user_password="root",
                                                             database_name=application_id+"_Database", database_port=3306,
                                                             init_database_script_path="./database/"+application_id+"/init_client_database.sql",
                                                             application_id=application_id)
        self.application_id = application_id
        self.start_time = datetime.datetime.strptime("00:00:01", "%H:%M:%S").time()
        self.end_time = datetime.datetime.strptime("23:59:59", "%H:%M:%S").time()
        self.client_fix_handler = ClientFIXHandler(self, self.client_database_handler)
        self.gui_handler = GUIHandler(self)
        self.gui_signal = GUISignal(self.gui_handler)

    def start_client(self):
        self.client_database_handler.init_database()
        self.gui_handler.start_gui()

    def logon(self):
        self.client_fix_handler.connect_to_server()
        return

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
        # OPTIONALTODO tobefixed not working comment it out to avoid error
        """
        five_smallest_offers_price, five_smallest_offers_quantity = self.extract_five_smallest_offers(offers_price,
                                                                                                      offers_quantity)
        five_biggest_bids_price, five_biggest_bids_quantity = self.extract_five_biggest_bids(bids_price, bid_quantity)
        """
        print offers_price, offers_quantity, bids_price, bid_quantity, current_price, current_quantity, opening_price, closing_price, day_high, day_low
        # OPTIONALTODO here should be some database interaction

        # OPTIONALTODO tobefixed not working comment it out to avoid error
        """
        order_book_buy = TradingClass.OrderBookBuy(five_biggest_bids_price, five_biggest_bids_quantity)
        order_book_sell = TradingClass.OrderBookBuy(five_smallest_offers_price, five_smallest_offers_quantity)
        """
        order_book_buy = TradingClass.OrderBookBuy([100, 200, 300, 400, 500], [10, 20, 30, 40, 50])
        order_book_sell = TradingClass.OrderBookBuy([100, 90, 80, 70, 60], [10, 11, 12, 13, 15, 16])
        stock_information = TradingClass.StockInformation(current_price, day_high, day_low)

        # OPTIONALTODO how todo date
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
            order_type (char/FIXHandlerUtils.OrderType)
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

    def process_order_execution_respond(self, execution_report):
        """ Processes execution report respond from the server side
        Args:
            execution_report (TradingClass.OrderExecution)
        Returns:
            None
        """
        if execution_report.execution_type == TradingClass.FIXHandlerUtils.ExecutionType.CANCELED:
            self.process_order_canceled_respond(execution_report)
        elif execution_report.execution_type == TradingClass.FIXHandlerUtils.ExecutionType.NEW:
            self.process_order_acknowlegded_respond(execution_report)
        elif execution_report.execution_type == TradingClass.FIXHandlerUtils.ExecutionType.REJECTED:
            self.process_order_rejected_respond(execution_report)
        elif execution_report.execution_type == TradingClass.FIXHandlerUtils.ExecutionType.PARTIAL_FILL:
            self.process_order_partial_filled_respond(execution_report)
        elif execution_report.execution_type == TradingClass.FIXHandlerUtils.ExecutionType.FILL:
            self.process_order_partial_filled_respond(execution_report)
        self.gui_handler.refresh_transactions()
        return

    def process_order_canceled_respond(self, execution_report):
        """ Processes an execution report regarding a canceled an order
        Args:
            execution_report (TradingClass.ExecutionReport)
        Returns:
            None
        """
        self.client_database_handler.update_order(execution_report.client_order_id,
                                                  order_status=TradingClass.DatabaseHandlerUtils.LastStatus.CANCELED)

    def process_order_acknowlegded_respond(self, execution_report):
        """ Processes an execution report regarding an acknowledged order
        Args:
            execution_report (TradingClass.ExecutionReport)
        Returns:
            None
        """
        self.client_database_handler.update_order(execution_report.client_order_id,
                                                  order_status=TradingClass.DatabaseHandlerUtils.LastStatus.PENDING)

    def process_order_rejected_respond(self, execution_report):
        """ Processes an execution report regarding a rejected order
        Args:
            execution_report (TradingClass.ExecutionReport)
        Returns:
            None
        """
        self.client_database_handler.update_order(execution_report.client_order_id,
                                                  order_status=TradingClass.DatabaseHandlerUtils.LastStatus.REJECTED)

    def process_order_partial_filled_respond(self, execution_report):
        """ Processes an execution report regarding partially filled order
        Args:
            execution_report (TradingClass.ExecutionReport)
        Returns:
            None
        """
        order = self.client_database_handler.fetch_order(execution_report.client_order_id)
        quantity_filled = order.order_quantity - execution_report.left_quantity
        self.client_database_handler.update_order(average_price=execution_report.average_price,
                                                  quantity_filled=quantity_filled)

    def process_order_cancel_request(self, order_id):
        """Processes a order cancel request before it is sent to the server
        Args:
            order_id (string): the id of the order which is requested to be canceled
        Returns:
            None
        """
        # Construct Fix Order Object to be sent to the fix handler
        cl_ord_id = self.client_database_handler.generate_new_cancel_order_id()
        client_order = self.client_database_handler.fetch_order(order_id)
        order_cancel_request = TradingClass.OrderCancelRequest.from_client_order(client_order, cl_ord_id)
        self.client_fix_handler.send_order_cancel_request(order_cancel_request)
        return

    def process_order_cancel_reject(self, order_cancel_reject):
        """
        Args
            order_cancel_request (TradingClass.OrderCancelReject)
        Return:
             None
        """
        pass

    def request_trading_transactions(self):
        client_orders = self.client_database_handler.fetch_all_order()

        order_id = []
        transaction_time = []
        side = []
        order_type = []
        order_price = []
        order_quantity = []
        last_status = []
        maturity_day = []
        quantity_filled = []
        average_price = []
        stock_ticker = []
        for order in client_orders:
            order_id.append(order.order_id)
            transaction_time.append(str(order.transaction_time))
            side.append(order.side)
            order_type.append(order.order_type)
            order_price.append(order.order_price)
            order_quantity.append(order.order_quantity)
            last_status.append(order.last_status)
            maturity_day.append(str(order.maturity_day))
            quantity_filled.append(order.quantity_filled)
            average_price.append(order.average_price)
            stock_ticker.append(order.stock_ticker)


        trading_transaction = TradingClass.TradingTransaction(order_id, transaction_time, side, order_type,
                                                              order_price, order_quantity,last_status,
                                                              maturity_day, quantity_filled, average_price,
                                                              stock_ticker)
        return trading_transaction

    def get_tomorrows_maturity_date(self):
        """Returns the standard maturity date which is the date of tomorrow
        Returns:
            maturity_date (FIXYearMonth)
            maturity_day (int): between 1-31
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        maturity_date = TradingClass.FIXYearMonth.from_year_month(tomorrow.year, tomorrow.month)
        maturity_day = tomorrow.day
        return maturity_date, maturity_day


class ClientDatabaseHandler(TradingClass.DatabaseHandler):
    """
    Attributes:
        application_id (string): the id used from the client, used to create an order id
    """
    last_market_data_request_id = 0

    def __init__(self, database_host, user_name, user_password, database_name,
                 database_port, init_database_script_path, application_id="client"):
        super(ClientDatabaseHandler, self).__init__(database_host, user_name, user_password, database_name,
                                                    database_port, init_database_script_path)
        self.application_id = application_id

    def generate_new_client_order_id(self):
        current_time = TradingClass.FIXDateTimeUTC.create_for_current_time()
        return self.application_id + "_" + str(current_time)

    def generate_new_cancel_order_id(self):
        return '1'

    def insert_order(self, order):
        """Inserts an order into client database
        Args:
            order (TradingClass.ClientOrder): order to be inserted
        Return:
            None
        """
        command = (
            "INSERT INTO `Order`(OrderID, TransactionTime, Side, OrderType, OrderQuantity, OrderPrice, LastStatus, "
            "MaturityDate, QuantityFilled, AveragePrice, StockTicker) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            % (order.order_id, order.transaction_time.mysql_date_stamp_string, str(order.side), str(order.order_type),
               str(order.order_quantity), str(order.order_price), str(order.last_status),
               order.maturity_day.mysql_date_stamp_string,
               str(order.quantity_filled), str(order.average_price), order.stock_ticker))
        self.execute_nonresponsive_sql_command(command)
        return

    def update_order(self, order_id, order_status=None, average_price=None, quantity_filled=None):
        """Changes the status of an order with order_id to order_status
        Args:
            order_id (string): the order id of the order where the status is changed
            order_status (int/TradingClass.DatabaseHandlerUtils.LastStatus): the new status for the order
            average_price (float) the new average price for the order
            quantity_filled (float) the new quantity fille for the order
        Return:
            None
        """
        sql_command = "UPDATE `Order` SET"
        set_part = []

        if order_status is not None: set_part.append(" LastStatus ='" + str(order_status) + "'")
        if average_price is not None: set_part.append(" AveragePrice ='" + str(average_price) + "'")
        if quantity_filled is not None: set_part.append(" QuantityFilled ='" + str(quantity_filled) + "'")

        if len(set_part) == 0:
            return

        for s in set_part:
            sql_command += s + ","

        # delete the last character: ","
        sql_command = sql_command[:len(sql_command) - 1]

        sql_command += (" where OrderID='%s'" % (order_id))
        self.execute_nonresponsive_sql_command(sql_command)

    def fetch_all_order(self):
        """Fetches all client order in client database
        Return:
            order[] (TradingClass.ClientOrder)
        """
        sql_command = ("select OrderID, TransactionTime, Side, OrderType, OrderQuantity, OrderPrice,"
                       "LastStatus, MaturityDate, QuantityFilled, AveragePrice, StockTicker from "
                       "`Order`")
        order_rows = self.execute_select_sql_command(sql_command)
        all_client_order=[]
        for order_row_list in order_rows:
            order_row_list = list(order_row_list)

            order_id = order_row_list[0]
            transaction_time = TradingClass.FIXDate(order_row_list[1])
            side = int(order_row_list[2])
            order_type = int(order_row_list[3])
            order_quantity = float(order_row_list[4])
            order_price = float(order_row_list[5])
            last_status = int(order_row_list[6])
            maturity_day = TradingClass.FIXDate(order_row_list[7])
            if order_row_list[8] == None:
                order_row_list[8] = 0
            quantity_filled = float(order_row_list[8])
            if order_row_list[9] == None:
                average_price=None
            else:
                average_price = float(order_row_list[9])
            stock_ticker = order_row_list[10]

            client_order = TradingClass.ClientOrder(order_id, transaction_time, side, order_type,
                                                    order_price, order_quantity, last_status, maturity_day,
                                                    quantity_filled, average_price, stock_ticker)
            all_client_order.append(client_order)
        return all_client_order


    def fetch_order(self, order_id):
        """Fetches an client order for a specific order id
        Args:
            order_id (string)
        Return:
            order (TradingClass.ClientOrder)
        """
        sql_command = ("select TransactionTime, Side, OrderType, OrderQuantity, OrderPrice,"
                       "LastStatus, MaturityDate, QuantityFilled, AveragePrice, StockTicker from "
                       "`Order` where OrderID='%s'") % (order_id)

        order_rows = self.execute_select_sql_command(sql_command)
        order_row_list = list(order_rows[0])

        transaction_time = TradingClass.FIXDate(order_row_list[0])
        side = int(order_row_list[1])
        order_type = int(order_row_list[2])
        order_quantity = float(order_row_list[3])
        order_price = float(order_row_list[4])
        last_status = int(order_row_list[5])
        maturity_day = TradingClass.FIXDate(order_row_list[6])
        if order_row_list[7]==None:
            order_row_list[7]=0
        if order_row_list[8] == None:
            order_row_list[8] = 0
        quantity_filled = float(order_row_list[7])
        average_price = float(order_row_list[8])
        stock_ticker = order_row_list[9]

        client_order = TradingClass.ClientOrder(order_id, transaction_time, side, order_type,
                                                order_price, order_quantity, last_status, maturity_day,
                                                quantity_filled, average_price, stock_ticker)
        return client_order

    def generate_market_data_request_id(self):
        self.last_market_data_request_id = self.last_market_data_request_id + 1
        return self.last_market_data_request_id

    def fetch_all_orders(self):
        """Returs all orders from the client

        Return:
             client_orders (list of TradingClass.ClientOrder)
        """
        client_orders = [TradingClass.ClientOrder.create_dummy_client_order()]
        return client_orders

class GUIHandler:
    def __init__(self, client_logic):
        """
        Args:
            client_logic (ClientLogic)
        """
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
            print ("input 1 to logon\ninput 2 to logout\ninput 3 to send market request\ninput 4 client exceeds 10 percent price gap\ninput 5"
             " client deceeds 10 percent price gap\ninput 6 client exceeds 20 percent of total tradable value\ninput 7 send an order which will"
            " be matched\ninput 8 client sends valid cancel request\ninput 9 client sends invalid cancel request\ninput 10 to quit")
            input = raw_input()
            if input == '1':
                self.client_logic.logon()
            elif input == '2':
                self.client_logic.logout()
            elif input == '3':
                self.send_market_data_request_option("TSLA")
            elif input == '4':
                self.client_exceeds_10_percent_price_gap()
            elif input == '5':
                self.client_deceeds_10_percent_price_gap()
            elif input == '6':
                self.client_exceeds_20_percent_total_tradable_value()
            elif input == '7':
                self.send_will_be_matched_order()
            elif input == '8':
                self.client_sends_valid_cancel_request()
            elif input == '9':
                self.client_sends_invalid_cancel_request()
            elif input == '10':
                break
            else:
                continue

    def refresh_transactions(self):
        """Refreshes the transaction list from the client"""
        trading_transactions_json = self.request_trading_transactions()
        self.client_logic.gui_signal.refreshTransaction(trading_transactions_json)

    def button_login_actuated(self):
        """This function is activated when the login button is pushed"""
        self.client_logic.logon()
        self.refresh_transactions()


    def button_cancel_actuated(self, order_id):
        """
        Args:
            order_id (unicode): the oid of the order requested to be canceled
        Return:
            None
        """
        self.client_logic.process_order_cancel_request(str(order_id))

    def request_trading_transactions(self):
        """Request trading transactions
        Returns:
        trading_transactions (string): json string of trading transaction
        """
        trading_transactions = self.client_logic.request_trading_transactions()
        # This function is needed, don't delete
        trading_transactions_json = self.extract_trading_transaction_json(trading_transactions)
        return trading_transactions_json

    def send_market_data_request_option(self, symbol):
        self.client_logic.process_market_data_request(symbol)

    # this function is used for button_buy_actuated as long it does not work
    def send_dummy_order(self):
        """For testing"""
        dummy_order = TradingClass.NewSingleOrder.create_dummy_new_single_order()
        self.client_logic.process_new_single_order_request(dummy_order.symbol, dummy_order.side, dummy_order.order_type,
                                                           dummy_order.price,
                                                           dummy_order.order_quantity)

    def send_order_cancel_request_option(self, order_id):
        self.client_logic.process_order_cancel_request(order_id)

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
        # OPTIONALTODO finish these functions
        quantity_chart_json = self.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.extract_course_chart_json(market_data)
        stock_information_json = self.extract_stock_information_json(market_data)
        order_book_json = self.extract_order_book_json(market_data)
        return quantity_chart_json, stock_course_chart_json, stock_information_json, order_book_json
        '''
        self.client_logic.gui_signal.refreshChart(market_data)

    def refresh_trading_transaction_list(self, trading_transaction):
        # This function is needed when fresh transaction list, don't delete it.
        trading_transactions_json=self.request_trading_transactions()
        self.client_logic.gui_signal.refreshTransaction(trading_transactions_json)

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
        for i in range(len(trading_transaction.order_id)):
            tmp = {}
            tmp["order_id"] = trading_transaction.order_id[i]
            tmp["transaction_time"] = trading_transaction.transaction_time[i]
            tmp["side"] = ("buy" if trading_transaction.side[i] == TradingClass.DatabaseHandlerUtils.Side.BUY else "sell")

            tmp["order_type"] =( "Market" if trading_transaction.order_type[i] ==
                                          TradingClass.DatabaseHandlerUtils.OrderType.MARKET else "Limit")

            tmp["order_price"] = trading_transaction.order_price[i]
            tmp["order_quantity"] = trading_transaction.order_quantity[i]

            if trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.DONE:
                tmp["last_status"] = "DONE"
            elif trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.PENDING:
                tmp["last_status"] = "PENDING"
            elif trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.CANCELED:
                tmp["last_status"] = "CANCELED"
            elif trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.EXPIRED:
                tmp["last_status"] = "EXPIRED"
            elif trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.NOT_YET_ACKNOWLEDGED:
                tmp["last_status"] = "NOT_YET_ACKNOWLEDGED"
            elif trading_transaction.last_status[i] == TradingClass.DatabaseHandlerUtils.LastStatus.REJECTED:
                tmp["last_status"] = "REJECTED"

            tmp["maturity_day"] = trading_transaction.maturity_day[i]
            tmp["quantity_filled"] = trading_transaction.quantity_filled[i]
            tmp["average_price"] = trading_transaction.average_price[i]
            tmp["stock_ticker"] = trading_transaction.stock_ticker[i]

            data["content"].append(tmp)

        return demjson.encode(data)

    def client_exceeds_10_percent_price_gap(self):
        """
        A client wants to send an order (more than) 10% more expensive than the last price
        """
        self.client_logic.process_new_single_order_request(stock_ticker="TSLA",
                                                           side=TradingClass.FIXHandlerUtils.Side.BUY,
                                                           order_type=TradingClass.FIXHandlerUtils.OrderType.LIMIT,
                                                           price=float(606),
                                                           quantity=float(10))

    def client_deceeds_10_percent_price_gap(self):
        """
        A client wants to send an order (more than) 10% less expensive than the last price
        """
        self.client_logic.process_new_single_order_request(stock_ticker="TSLA",
                                                           side=TradingClass.FIXHandlerUtils.Side.BUY,
                                                           order_type=TradingClass.FIXHandlerUtils.OrderType.LIMIT,
                                                           price=float(494),
                                                           quantity=float(10))

    def client_exceeds_20_percent_total_tradable_value(self):
        """
		A client wants to send an order that represents more than 20% of the total tradable value
        """ 
        self.client_logic.process_new_single_order_request(stock_ticker="TSLA",
                                                           side=TradingClass.FIXHandlerUtils.Side.BUY,
                                                           order_type=TradingClass.FIXHandlerUtils.OrderType.LIMIT,
                                                           price=float(500),
                                                           quantity=float(34))
        pass

    def send_will_be_matched_order(self):
        self.client_logic.process_new_single_order_request(stock_ticker="MS",
                                                           side=TradingClass.FIXHandlerUtils.Side.SELL,
                                                           order_type=TradingClass.FIXHandlerUtils.OrderType.LIMIT,
                                                           price=float(560),
                                                           quantity=float(10))
    def client_sends_valid_cancel_request(self):
        self.client_logic.process_order_cancel_request("client_20161109-10:40:00")
        pass

    def client_sends_invalid_cancel_request(self):
        client_order = TradingClass.ClientOrder.create_dummy_client_order(order_id="wrong_id")
        order_cancel_request = TradingClass.OrderCancelRequest.from_client_order(client_order, "new_id")
        self.client_logic.client_fix_handler.send_order_cancel_request(order_cancel_request)
