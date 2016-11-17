import sys
import quickfix as fix
from quickfix import Side_BUY, Side_SELL
import quickfix42 as fix42
import TradingClass
from TradingClass import MarketDataResponse
from TradingClass import OrderExecution
from TradingClass import FIXOrder
from TradingClass import FIXDate
from TradingClass import YearMonthFix
from TradingClass import FIXDateTimeUTC
from TradingClass import FIXTime
import pdb
import htmlPy
import json
import demjson

sys.path.append('GUI')
from frontEnd import htmlPy_app
import numpy as np


class GUISignal(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    def __init__(self,c_l):
        super(GUISignal, self).__init__()
        self.client_logic = c_l
        self.fresh=1;
        # Initialize the class here, if required.
        return

    @htmlPy.Slot(str, str, result=str)
    def logIn(self, usr, psw):
        # login
        usr = str(usr)
        psw = str(psw)
        print usr, psw
        if (self.client_logic.gui_handler.button_login_actuated(usr, psw)):
            return_message = '{"success":true,"userName":"' + usr + '"}'
        else:
            return_message = '{"success":false,"msg":"username or password is wrong"}'
        return return_message

    @htmlPy.Slot()
    def logOut(self):
        self.client_logic.gui_handler.button_logout_actuated()

    @htmlPy.Slot(str)
    def searchStock(self, stockCode):
        self.client_logic.gui_handler.search_for_stock_actuated(stockCode)

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


        quantity_chart_json = self.client_logic.gui_handler.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.client_logic.gui_handler.extract_course_chart_json(market_data)
        stock_information_json = self.client_logic.gui_handler.extract_stock_information_json(market_data)
        order_book_json = self.client_logic.gui_handler.extract_order_book_json(market_data)

        #trading_transaction_json = self.client_logic.gui_handler.extract_trading_transaction_json(trading_transaction)
        result = '{' + '"success":true' + ',"quantity":' + quantity_chart_json + ',"price":' + stock_course_chart_json + ',"stockInfo":' + stock_information_json + ',"orderBook":' + order_book_json + '}'
        htmlPy_app.evaluate_javascript("freshChart('"+result+"')")

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


class ClientFIXHandler(TradingClass.FIXHandler):
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
        self.client_database_handler = ClientDatabaseHandler()
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

    def connect_to_server(self, user_id, password):
        self.set_user_id(user_id)
        self.set_password(password)
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def handle_to_be_sent_logon_request(self, message):
        """Handle a logon request which is about to be sent

        Before the logon request is sent to the server, this function handles the message and modifies fields.

        Args:
            message (Swig Object of type 'FIX::Message *'): the message to be sent
        """
        self.add_user_id_to_message(message)
        self.add_password_to_message(message)
        # TODO @alex flush password
        # self.fix_application.del_user_id()
        # self.fix_application.del_password()

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
        header.setField(fix.MsgSeqNum(self.client_database_handler.generate_new_order_id()))
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

        a_date = TradingClass.FIXDate.from_year_month_day(2000, 1, 1)
        a_time = FIXTime(0, 0, 0)
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
        market_data = MarketDataResponse(md_req_id_fix.getValue(), no_md_entries_fix.getValue(), symbol_fix.getValue()
                                         , md_entry_type_list, md_entry_px_list, md_entry_size_list, md_entry_date_list,
                                         md_entry_time_list)

        self.client_logic.process_market_data_respond(market_data)
        pass

    def send_order(self, fix_order):
        """Sends an order to server based on fix_order object created in client_logic

        TODO @husein description if needed

        Args:
            order (class order): s

        Returns:

        """

        # Create Fix Message for Order
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.SenderCompID(fix_order.get_sender_comp_id()))
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgSeqNum(self.fix_application.order_id))
        header.setField(fix.SendingTime())

        # Set Fix Message fix_order object
        maturity_month_year_fix = fix.MaturityMonthYear()
        maturity_month_year_fix.setString(fix_order.get_maturity_month_year().__str__())
        transact_time_fix = fix.TransactTime()
        transact_time_fix.setString(fix_order.get_transact_time().__str__())

        message.setField(fix.ClOrdID(str(fix_order.get_cl_ord_id())))
        message.setField(fix.HandlInst(fix_order.get_handl_inst()))
        message.setField(fix.ExecInst(fix_order.get_exec_inst()))  # 2 allow partial order, G All or None
        message.setField(fix.Symbol(fix_order.get_symbol()))
        message.setField(maturity_month_year_fix)
        message.setField(fix.MaturityDay(str(fix_order.get_maturity_day())))
        message.setField(fix.Side(fix_order.get_side()))  # 1 buy, 2 sell
        message.setField(transact_time_fix)
        message.setField(fix.OrderQty(fix_order.get_order_qty()))
        message.setField(fix.OrdType(
            fix_order.get_ord_type()))  # 1 = Market, 2 = Limit,3 = Stop // optional,4 = Stop limit // optional,
        message.setField(fix.Price(fix_order.get_price()))
        message.setField(fix.StopPx(fix_order.get_stop_px()))

        # Send Fix Message to Server
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

        return

    def handle_execution_report(self, message):
        order_id_fix = fix.OrderID()
        cl_ord_id_fix = fix.ClOrdID()
        exec_id_fix = fix.ExecID()
        exec_trans_type_fix = fix.ExecTransType()
        exec_type_fix = fix.ExecType()
        ord_status_fix = fix.OrdStatus()
        symbol_fix = fix.Symbol()
        side_fix = fix.Side()
        leaves_qty_fix = fix.LeavesQty()
        cum_qty_fix = fix.CumQty()
        avg_px_fix = fix.AvgPx()
        price_fix = fix.Price()
        stop_px_fix = fix.StopPx()

        message.getField(cl_ord_id_fix)
        message.getField(order_id_fix)
        message.getField(exec_id_fix)
        message.getField(exec_trans_type_fix)
        message.getField(exec_type_fix)
        message.getField(ord_status_fix)
        message.getField(symbol_fix)
        message.getField(side_fix)
        message.getField(leaves_qty_fix)
        message.getField(cum_qty_fix)
        message.getField(avg_px_fix)
        message.getField(price_fix)
        message.getField(stop_px_fix)

        # Encapsulate result of receiving execution report into order execution report
        order_execution = OrderExecution(order_id_fix.getValue(), cl_ord_id_fix.getValue(), exec_id_fix.getValue()
                                         , exec_trans_type_fix.getValue(), exec_type_fix.getValue(),
                                         ord_status_fix.getValue(), symbol_fix.getValue()
                                         , side_fix.getValue(), leaves_qty_fix.getValue(), cum_qty_fix.getValue(),
                                         avg_px_fix.getValue()
                                         , price_fix.getValue(), stop_px_fix.getValue())

        self.client_logic.process_order_execution_respond(order_execution)

        return

    def add_user_id_to_message(self, message):
        message.setField(fix.RawData(self.get_password()))
        message.setField(fix.RawDataLength(len(self.get_password())))

    def add_password_to_message(self, message):
        message.getHeader().setField(fix.SenderSubID(self.get_user_id()))

    def send_logout_request(self):
        self.socket_initiator.stop()

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_password(self, password):
        self.password = password

    def get_user_id(self):
        return self.user_id

    def get_password(self):
        return self.password

    def del_user_id(self):
        del self.user_id

    def del_password(self):
        del self.password


class ClientLogic():
    def __init__(self, client_config_file_name):
        self.client_fix_handler = ClientFIXHandler(self, client_config_file_name)
        self.client_database_handler = ClientDatabaseHandler()
        self.gui_signal = GUISignal(self)
        self.gui_handler = GUIHandler(self)

    def start_client(self):
        # start some gui stuff and other things, for now only gui
        self.gui_handler.start_gui()

    def logon(self, user_id, password):
        self.client_fix_handler.connect_to_server(user_id, password)

        # TODO block mechanism
        self.block_gui()

        # return self.success

        # Notice that we should validate here
        return True

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
        print market_data.get_no_md_entry_types()
        print market_data.get_symbol()
        for j in range(market_data.get_no_md_entry_types()):
            print(market_data.get_md_entry_type(j))
            print(market_data.get_md_entry_px(j))
            print(market_data.get_md_entry_size(j))
            print(market_data.get_md_entry_date(j))
            print(market_data.get_md_entry_time(j))

        offers_price, offers_quantity, bids_price, bid_quantity, current_price, current_quantity, opening_price, \
        closing_price, day_high, day_low = self.extract_market_data_information(market_data)
        five_smallest_offers_price, five_smallest_offers_quantity = self.extract_five_smallest_offers(offers_price,
                                                                                                      offers_quantity)
        five_biggest_bids_price, five_biggest_bids_quantity = self.extract_five_biggest_bids(bids_price, bid_quantity)

        #TODO here should be some database interaction

        order_book_buy = TradingClass.OrderBookBuy(five_biggest_bids_price, five_biggest_bids_quantity)
        order_book_sell = TradingClass.OrderBookBuy(five_smallest_offers_price, five_smallest_offers_quantity)
        stock_information = TradingClass.StockInformation(current_price, day_high, day_low)

        # TODO how todo date
        stock_history = TradingClass.StockHistory(market_data.get_md_entry_date, current_price, current_quantity)
        gui_market_data = TradingClass.MarketData(stock_information, stock_history, order_book_buy, order_book_sell)

        self.gui_handler.refresh_charts(gui_market_data)

        return

    def process_order_request(self, order):
        # Get Order instruction from GUI
        # Left Blank

        # Construct Fix Order Object to be sent to the fix handler
        cl_ord_id = self.client_fix_handler.fix_application.gen_order_id()
        handl_inst = '1'
        exec_inst = '2'
        symbol = 'MS'
        maturity_month_year = YearMonthFix(2016, 1)
        maturity_day = 1
        side = Side_BUY
        transact_time = FIXDateTimeUTC(2016, 1, 1, 11, 40, 10)
        order_qty = 10
        ord_type = '1'
        price = 20
        stop_px = 10000
        sender_comp_id = "client"
        sending_time = None
        on_behalf_of_comp_id = None
        sender_sub_id = None

        fix_order = FIXOrder(cl_ord_id, handl_inst, exec_inst, symbol, maturity_month_year, maturity_day, side
                             , transact_time, order_qty, ord_type, price, stop_px, sender_comp_id, sending_time,
                             on_behalf_of_comp_id
                             , sender_sub_id)
        self.client_fix_handler.send_order(fix_order)
        return

    def process_order_execution_respond(self, order_execution):
        # process execution respond from server

        print("exec_id_fix, exec_trans_type_fix,exec_type_fix,ord_status_fix,symbol_fix,side_fix,eaves_qty_fix,"
              "cum_qty_fix,avg_px_fix,price_fix,stop_px_fix,")
        print(order_execution.get_order_id())
        print(order_execution.get_exec_id())
        print(order_execution.get_exec_trans_type())
        print(order_execution.get_exec_type())
        print(order_execution.get_ord_status())
        print(order_execution.get_symbol())
        print(order_execution.get_side())
        print(order_execution.get_leaves_qty())
        print(order_execution.get_cum_qty())
        print(order_execution.get_avg_px())
        print(order_execution.get_price())
        print(order_execution.get_stop_px())
        return

    def request_trading_transactions(self, user_name):
        # TODO alex write database request/fetch
        # TODO FIRST yelinsheng sample data
        trading_transaction = None
        return trading_transaction

    def extract_offers_price_quantity(self, market_data_entry_types, market_data_entry_prices,
                                      market_data_entry_quantity):
        prices = market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_OFFER]
        quantity = market_data_entry_quantity[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_OFFER]
        return prices, quantity

    def extract_bids_price_quantity(self, market_data_entry_types, market_data_entry_prices,
                                    market_data_entry_quantity):
        prices = market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_BIDS]
        quantity = market_data_entry_quantity[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_BIDS]
        return prices, quantity

    def extract_current_price(self, market_data_entry_types, market_data_entry_prices):
        current_price = \
            market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_CURRENT_PRICE][0]
        return current_price

    def extract_opening_price(self, market_data_entry_types, market_data_entry_prices):
        opening_price = \
            market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_OPENING_PRICE][0]
        return opening_price

    def extract_closing_price(self, market_data_entry_types, market_data_entry_prices):
        closing_price = \
            market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_CLOSING_PRICE][0]
        return closing_price

    def extract_day_high(self, market_data_entry_types, market_data_entry_prices):
        session_high = market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_DAY_HIGH][
            0]
        return session_high

    def extract_day_low(self, market_data_entry_types, market_data_entry_prices):
        session_low = market_data_entry_prices[market_data_entry_types == self.client_fix_handler.ENTRY_TYPE_DAY_LOW][0]
        return session_low

    def extract_market_data_information(self, market_data):
        market_data_entry_types = np.array(market_data.get_md_entry_type_list())
        market_data_entry_prices = np.array(market_data.get_md_entry_px_list())
        market_data_entry_quantity = np.array(market_data.get_md_entry_size_list())

        offers_price, offers_quantity = self.extract_offers_price_quantity(market_data_entry_types,
                                                                           market_data_entry_prices,
                                                                           market_data_entry_quantity)
        bids_price, bids_quantity = self.extract_bids_price_quantity(market_data_entry_types, market_data_entry_prices,
                                                                     market_data_entry_quantity)
        current_price = self.extract_current_price(market_data_entry_types, market_data_entry_prices)
        current_quantity = market_data.get_md_total_volume_traded()
        opening_price = self.extract_opening_price(market_data_entry_types)
        closing_price = self.extract_closing_price(market_data_entry_types)
        day_high = self.extract_day_high(market_data_entry_types)
        day_low = self.extract_low_low(market_data_entry_types)

        offers_price, offers_quantity, bids_price, bids_quantity, current_price, current_quantity, opening_price, \
        closing_price, day_high, day_low = \
            transform_numpy_array_to_list(offers_price, offers_quantity, bids_price, bids_quantity, current_price,
                                          current_quantity, opening_price, closing_price, day_high, day_low)
        return offers_price, offers_quantity, bids_price, bids_quantity, current_price, current_quantity, opening_price, \
               closing_price, day_high, day_low


    def extract_five_smallest_offers(self, offers_price, offers_quantity):
        five_smallest_offers_indices = extract_n_smallest_indices(offers_price, 5)
        five_smallest_offers_price, five_smallest_offers_quantity = \
            get_values_from_lists_for_certain_indices(five_smallest_offers_indices, offers_price, offers_quantity)
        return five_smallest_offers_price, five_smallest_offers_quantity


    def extract_five_biggest_bids(self, bids_price, bids_quantity):
        five_biggest_bids_indices = extract_n_biggest_indices(bids_price)
        five_biggest_bids_price, five_biggest_bids_quantity = get_values_from_lists_for_certain_indices(
            five_biggest_bids_indices, bids_price, bids_quantity)
        return five_biggest_bids_price, five_biggest_bids_quantity


def extract_n_smallest_indices(integer_list, n, order="ascending"):
    n_smallest_indices = np.argsort(integer_list)[:n]
    if order == "descending":
        n_smallest_indices = n_smallest_indices[::-1]

    return n_smallest_indices


def extract_n_biggest_indices(integer_list, n, order="ascending"):
    n_biggest_indices = np.argsort(integer_list)[-n:]
    if order == "descending":
        n_biggest_indices = n_biggest_indices[::-1]
    return n_biggest_indices


def get_values_from_lists_for_certain_indices(certain_indices, *lists):
    values_of_lists = []
    for list_ in lists:
        values_of_lists.append(list(np.array(list_)[certain_indices]))
    return values_of_lists


def transform_numpy_array_to_list(*numpy_arrays):
    lists = []
    for numpy_array in numpy_arrays:
        lists.append(list(numpy_array))
    return lists




class ClientDatabaseHandler:
    last_order_id = 0
    last_market_data_request_id = 0

    # TODO not threadsafe, but anyway it should be mysql request
    def generate_new_order_id(self):
        self.last_order_id = self.last_order_id + 1
        return self.last_order_id

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
                file = open("rawData.json", "r")
                rawData = file.read()
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
            print '''input 1 to logon\ninput 2 to logout\ninput 3 to send market request\ninput 4 to order\ninput 5 to quit'''
            input = raw_input()
            if input == '1':
                self.button_login_actuated("john", "papapa")
            elif input == '2':
                self.button_logout_actuated()
            elif input == '3':
                self.send_market_data_request_option("TSLA")
            elif input == '4':
                self.send_order_request_option("order")
            elif input == '5':
                break
            else:
                continue

    def button_login_actuated(self, user_name, user_password):
        """This function is activated when the login button is pushed"""
        return self.client_logic.logon(user_name, user_password)

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

    def send_order_request_option(self, order):
        self.client_logic.process_order_request(order)

    def button_buy_actuated(self, stock_ticker, price, quantity):
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
        print "Request market data for "+stock_ticker_symbol
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
