import sys
import quickfix as fix
from quickfix import Side_BUY, Side_SELL
import quickfix42 as fix42
from TradingClass import MarketDataResponse
import pdb
import htmlPy
import json
sys.path.append('GUI')
from frontEnd import htmlPy_app

class GUISignal(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    def __init__(self,g):
        super(GUISignal,self).__init__()
        self.gui_handler=g
        # Initialize the class here, if required.
        return

    @htmlPy.Slot(str,str,result=str)
    def logIn(self,usr,psw):
        #login
        usr=str(usr)
        psw=str(psw)
        print usr,psw
        if(self.gui_handler.button_login_actuated(usr,psw)):
            return_message='{"success":true,"userName":"'+usr+'"}'
        else:
            return_message='{"success":false,"msg":"username or password is wrong"}'
        return return_message

    @htmlPy.Slot()
    def logOut(self):
        self.gui_handler.button_logout_actuated()


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
        self.sessionID=session_id

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
        if(msg_Type.getString() ==fix.MsgType_MarketDataSnapshotFullRefresh):
            print "MarketDataSnapshotFullRefresh"
            self.client_fix_handler.handle_market_data_respond(message)

        if(msg_Type.getString() ==fix.MsgType_ExecutionReport):
            print "ExecutionReport"
            self.client_fix_handler.handle_execution_report(message)

    def toApp(self, message, session_id):
        print "OUT", message

    def _calculate_checksum(self):
        pass

    def gen_order_id(self):
        self.order_id = self.order_id+1
        return self.order_id

    def gen_market_data_request_id(self):
        self.market_data_request_id = self.market_data_request_id+1
        return self.market_data_request_id


class ClientFIXHandler():
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
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

    def send_market_data_request(self,symbol):
        """Sends a market data request to server

        TODO @husein description if needed

        Args:
            symbol (string): the ticker symbol of a stock

        Returns:

        """
        #Create Fix Message for Market Data Request
        message = fix.Message();
        header = message.getHeader();
        header.setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        header.setField(fix.MsgSeqNum(self.fix_application.order_id))
        header.setField(fix.SendingTime())
        message.setField(fix.MDReqID(str(self.fix_application.gen_market_data_request_id())))
        message.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT))
        message.setField(fix.MarketDepth(1))
        message.setField(fix.NoMDEntryTypes(10))

        group_md_entry= fix42.MarketDataRequest().NoMDEntryTypes()
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

        #Send Fix Message to Server
        fix.Session.sendToTarget(message,self.fix_application.sessionID)

        return

    def handle_market_data_respond(self, message):
        """Handles market data respond

        TODO @husein description if needed

        Args:
            message (FIX::Message): Market data message to be handled.

        Returns:
            TODO how does the return value look like
        """

        #Retrieve Market Data Response Type Full Refresh/Snapshot
        md_req_id_fix = fix.MDReqID()
        no_md_entries_fix= fix.NoMDEntries()
        symbol_fix=fix.Symbol()
        md_entry_type_fix=fix.MDEntryType()
        md_entry_px_fix=fix.MDEntryPx()
        md_entry_size_fix=fix.MDEntrySize()
        md_entry_date_fix=fix.MDEntryDate()
        md_entry_time_fix=fix.MDEntryTime()
        md_entry_type_list=[]
        md_entry_px_list=[]
        md_entry_size_list=[]
        md_entry_date_list=[]
        md_entry_time_list=[]

        message.getField(md_req_id_fix)
        message.getField(no_md_entries_fix)
        message.getField(symbol_fix)

        groupMD= fix42.MarketDataSnapshotFullRefresh.NoMDEntries()
        for MDIndex in range(no_md_entries_fix.getValue()):
            message.getGroup(MDIndex+1,groupMD)
            groupMD.getField(md_entry_type_fix)
            groupMD.getField(md_entry_px_fix)
            groupMD.getField(md_entry_size_fix)
            groupMD.getField(md_entry_date_fix)
            groupMD.getField(md_entry_time_fix)
            md_entry_type_list.append(md_entry_type_fix.getValue())
            md_entry_px_list.append(md_entry_px_fix.getValue())
            md_entry_size_list.append(md_entry_size_fix.getValue())
            md_entry_date_list.append(md_entry_date_fix.getString())
            md_entry_time_list.append(md_entry_time_fix.getString())

        #Encapsulate data into market data response object
        market_data= MarketDataResponse(md_req_id_fix.getValue(), no_md_entries_fix.getValue(), symbol_fix.getValue()
            , md_entry_type_list, md_entry_px_list, md_entry_size_list, md_entry_date_list, md_entry_time_list)

        #Should be done in client gui or client logic can be moved by passing object to another class for now as example
        print "tes1"
        print market_data.get_no_md_entry_types()
        print market_data.get_symbol()
        for j in range (market_data.get_no_md_entry_types()):
            print(market_data.get_md_entry_type_list()[j])
            print(market_data.get_md_entry_px_list()[j])
            print(market_data.get_md_entry_size_list()[j])
            print(market_data.get_md_entry_date_list()[j])
            print(market_data.get_md_entry_time_list()[j])
        print "tes2"
        pass

    def send_order(self, order):
        """Sends an order to server

        TODO @husein description if needed

        Args:
            order (class order): s

        Returns:

        """

        #First Retrieve Input From GUI using order object
        #                 Left Blank

        #Create Fix Message for Order
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        header.setField(fix.MsgSeqNum(self.fix_application.order_id))
        header.setField(fix.SendingTime())

        #Set Message with ExecInst 2, Side Buy and Ord Type Market
        message.setField(fix.ClOrdID(str(self.fix_application.gen_order_id())))
        message.setField(fix.HandlInst('1'))
        message.setField(fix.ExecInst('2')) #2 allow partial order, G All or None
        message.setField(fix.Symbol("XEN"))
        message.setField(fix.Side(Side_BUY)) #1 buy, 2 sell
        message.setField(fix.MaturityMonthYear("201601"))
        message.setField(fix.MaturityDay("20"))
        message.setField(fix.TransactTime())
        message.setField(fix.OrderQty(10))
        message.setField(fix.OrdType('1')) #1 = Market, 2 = Limit,3 = Stop // optional,4 = Stop limit // optional,
        message.setField(fix.Price(1000))
        message.setField(fix.StopPx(10000))

        #Send Fix Message to Server
        fix.Session.sendToTarget(message,self.fix_application.sessionID)

        #Simulate possible Order Type with Side=Buy and Exec Inst =2
        for i in range(3):
            message.setField(fix.OrdType(str(i+2)))
            fix.Session.sendToTarget(message,self.fix_application.sessionID)
        #Simulate possible Order Type with Side=Buy and Exec Inst =G
        message.setField(fix.ExecInst('G'))
        for j in range(4):
            message.setField(fix.OrdType(str(j+1)))
            fix.Session.sendToTarget(message,self.fix_application.sessionID)

        #Set Order with Side Sell
        message.setField(fix.Side(Side_SELL)) #1 buy, 2 sell

        #Simulate Order Type with Sell and Exec Inst =2
        message.setField(fix.ExecInst('2'))
        for k in range(4):
            message.setField(fix.OrdType(str(k+1)))
            fix.Session.sendToTarget(message,self.fix_application.sessionID)
        #Simulate Order Type with Buy and Exec Inst =G
        message.setField(fix.ExecInst('G'))
        for l in range(4):
            message.setField(fix.OrdType(str(l+1)))
            fix.Session.sendToTarget(message,self.fix_application.sessionID)

        return

    def handle_execution_report(self,message):

        order_id_fix = fix.ClOrdID()
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

        #Suppose this should be done in client logic/ GUI
        print("exec_id_fix, exec_trans_type_fix,exec_type_fix,ord_status_fix,symbol_fix,side_fix,eaves_qty_fix,"
              "cum_qty_fix,avg_px_fix,price_fix,stop_px_fix,")
        print(order_id_fix.getValue())
        print(exec_id_fix.getValue())
        print(exec_trans_type_fix.getValue())
        print(exec_type_fix.getValue())
        print(ord_status_fix.getValue())
        print(symbol_fix.getValue())
        print(side_fix.getValue())
        print(leaves_qty_fix.getValue())
        print(cum_qty_fix.getValue())
        print(avg_px_fix.getValue())
        print(price_fix.getValue())
        print(stop_px_fix.getValue())

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
        self.gui_handler = GUIHandler(self)

    def start_client(self):
        # start some gui stuff and other things, for now only gui
        self.gui_handler.start_gui()

    def logon(self, user_id, password):

        self.client_fix_handler.connect_to_server(user_id, password)

        #TODO block mechanism
        self.block_gui()

        #return self.success

        #Notice that we should validate here
        return True

    def block_gui(self):
        pass

    def logout(self):
        self.client_fix_handler.send_logout_request()

    def process_market_data_request(self, symbol):
        self.client_fix_handler.send_market_data_request(symbol)

    def process_market_data_respond(self, marketData):
        """Process market data respond

        Args:
            message (list of str): .

        Returns:
            None
        """
        return

    def process_order_request(self,order):
        self.client_fix_handler.send_order(order)
        return

    def request_trading_transactions(self, user_name):
        #TODO alex write database request/fetch
        #TODO FIRST yelinsheng sample data
        trading_transaction = None
        return trading_transaction


class GUIHandler:
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        while(True):
            print '''input 1 to run in terminal\ninput 2 to start gui\ninput 3 to quit'''
            input = raw_input()
            #input='2'
            if(input=='1'):
                self.wait_for_input()
            elif(input=='2'):
                file=open("rawData.json","r")
                rawData=file.read()
                json={
                    "rawData":rawData
                }
                htmlPy_app.template = ("index.html", json)
                htmlPy_app.bind(GUISignal(self))
                htmlPy_app.start()
            elif(input=='3'):
                break
            else:
                continue


    def wait_for_input(self):
        while True:
            print '''input 1 to logon\ninput 2 to logout\ninput 3 to send market request\ninput 4 to order\ninput 5 to quit'''
            input = raw_input()
            if input == '1':
                self.button_login_actuated("john","papapa")
            elif input == '2':
                self.button_logout_actuated()
            elif input == '3':
                self.send_market_data_request_option("CNNA")
            elif input =='4':
                self.send_order_request_option("order")
            elif input =='5':
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
        #TODO yenlinsheng finish this function
        trading_transactions_json = self.extract_trading_transactions_json(trading_transactions)
        pass

    def button_logout_actuated(self):
        """This function is activated when the login button is pushed"""
        respond = self.client_logic.logout()

#<<<<<<< HEAD
    def send_market_data_request_option(self, symbol):
        self.client_logic.process_market_data_request(symbol)

    def send_order_request_option(self, order):
        self.client_logic.process_order_request(order)

#=======
    def button_buy_actuated(self, stock_ticker, price, quantity):
        #TODO alex
        pass

    def search_for_stock_actuated(self, searching_value):
        """This function is called when the user enters a search request

        Args:
            searching_value (string): The value of the user input

        Returns:
            None
        """
        #TODO alex
        pass

    def refresh_charts(self, market_data):
        #TODO yenlinsheng finish these functions
        quantity_chart_json = self.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.extract_course_chart_json(market_data)
        stock_information_json =  self.extract_stock_information_json(market_data)
        order_book_json = self.extract_order_book_json(market_data)
        pass

    def refresh_trading_transaction_list(self, trading_transaction):
        #TODO yenlinsheng finish this function
        trading_transaction_json = self.extract_trading_transaction_json(trading_transaction)
        pass
    def extract_quantity_chart_json(self,market_data):
        pass
    def extract_course_chart_json(market_data):
        pass
    def extract_stock_information_json(market_data):
        pass
    def extract_order_book_json(market_data):
        pass
    def extract_trading_transaction_json(trading_transaction):
        pass

#TODO FIRST yenlinsheng MarketData class
#DONE by yelinsheng 2016-10-28
class StockInformation():
    def __init__(self,p_price,p_high,p_low):
        self.price=p_price
        self.high=p_high
        self.low=p_low
class StockHistory():
    def __init__(self,p_time,p_price,p_quantity):
        #time,price,quantity are list type
        self.time=p_time
        self.price=p_price
        self.quantity=p_quantity
class OrderBookBuy():
    def __init__(self,p_price,p_quantity):
        #price,quantity are list type, with length of 5
        self.price=p_price
        self.quantity=p_quantity
class OrderBookSell():
    def __init__(self,p_price,p_quantity):
        #price,quantity are list type, with length of 5
        self.price=p_price
        self.quantity=p_quantity
class MarketData():
    def __init__(self,p_stock_information,p_stock_history,p_order_book_buy,p_order_book_sell):
        #type of parameters:
        #stock_information -> StockInformation
        #stock_history -> StockHistory
        #order_book_buy -> OrderBookBuy
        #order_book_sell -> OrderBookSell
        self.stock_information=p_stock_information
        self.stock_history=p_stock_history
        self.order_book_buy=p_order_book_buy
        self.order_book_sell=p_order_book_sell


#TODO FIRST yelinsheng TradingTransaction class
#DONE by yelinsheng 2016-10-28
class TradingTransaction():
    def __init__(self,p_time,p_price,p_quantity,p_side):
        #side: True means buy, False means sell 
        self.time=p_time
        self.price=p_price
        self.quantity=p_quantity
        self.side=p_side


#>>>>>>> add_matching_algorithm_outline

client_config_file_name = sys.argv[1] if len(sys.argv) == 2 else "client.cfg"
client = ClientLogic(client_config_file_name)
client.start_client()
