import quickfix as fix
import quickfix42 as fix42
import sys
import time
import pdb
import yahoo_finance
import MySQLdb
from enum import Enum
from TradingClass import MarketDataRequest
from TradingClass import MarketDataResponse

class ServerRespond(Enum):
    AUTHENTICATION_FAILED = 0
    AUTHENTICATION_SUCCESS = 1


class ServerFIXApplication(fix.Application):
    def __init__(self, server_fix_handler):
        self.server_fix_handler = server_fix_handler
        super(ServerFIXApplication, self).__init__()

    def onCreate(self, session_id):
        self.sessionID=session_id
        return

    def onLogon(self, session_id):
        return

    def onLogout(self, session_id):
        return

    def toAdmin(self, message, session_id):
        return

    def fromAdmin(self, message, session_id):
        """React to admin level messages

        This function is invoked when administrative message is received. For example: Logon, Logout, Heartbeat.
        TODO what is a administrative message?

        Args:
            message (Swig Object of type 'FIX::Message *'): The received message
            session_id (Swig Object of type 'FIX::SessionID *'): The received message

        Returns:
            None
        """

        # begin_string = message.getHeader().getField(fix.BeginString())  # returns 'FIX::FieldBase *'
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type.getString() == fix.MsgType_Logon:
            self.server_fix_handler.handle_logon_request(message)
        else:
            # TODO send error: MsgType not understand
            pass

        return

    def toApp(self, message, session_id):
        return

    def fromApp(self, message, session_id):
        """React to application level messages

        This function is invoked when a application level request is received.
        TODO What is a application level request?

        Args:
            message (Swig Object of type 'FIX::Message *'): The received message
            session_id (Swig Object of type 'FIX::SessionID *'): The received message

        Returns:
            None
        """
        # beginString = message.getHeader().getField(fix.BeginString())
        msg_Type = message.getHeader().getField(fix.MsgType())
        if msg_Type.getString() ==fix.MsgType_MarketDataRequest:
            print '''IN MarketDataRequest'''
            self.server_fix_handler.handle_market_data_request(message)



class ServerFIXHandler:
    def __init__(self, server_logic, server_config_file_name):
        self.server_logic = server_logic
        self.server_config_file_name = server_config_file_name
        self.fix_application = None
        self.socket_acceptor = None

    def start(self):
        self.init_fix_settings()
        self.socket_acceptor.start()

    def stop(self):
        self.socket_acceptor.stop()

    def init_fix_settings(self):
        settings = fix.SessionSettings(self.server_config_file_name)
        self.fix_application = ServerFIXApplication(self)
        self.storeFactory = fix.FileStoreFactory(settings)
        # logFactory = fix.FileLogFactory(settings)
        self.logFactory = fix.ScreenLogFactory(settings)
        self.socket_acceptor = fix.SocketAcceptor(self.fix_application, self.storeFactory, settings, self.logFactory)

    def handle_logon_request(self, message):
        password = message.getField(fix.RawData())
        user_id = message.getHeader().getField(fix.SenderSubID())
        logon_respond = self.server_logic.process_logon(user_id, password)
        if logon_respond == ServerRespond.AUTHENTICATION_FAILED:
            # TODO reject client AUTHENTICATION_FAILED
            pass

        return

    def handle_market_data_request(self, message):
        """Process market data request
            TODO @husein

    		Args:
    			symbols (list of str): A list of symbol tickers.

    		Returns:
    			None
    		"""
        #Retrieving Fix Data from market data request sent by client
        mdReqID = fix.MDReqID()
        subscriptionRequestType = fix.SubscriptionRequestType()
        marketDepth = fix.MarketDepth()
        mdUpdateType = fix.MDUpdateType()
        noMDEntryType = fix.NoMDEntryTypes()
        mdEntryType= fix.MDEntryType()
        noRelatedSym= fix.NoRelatedSym()

        message.getField(mdReqID)
        message.getField(subscriptionRequestType)
        message.getField(marketDepth)
        message.getField(mdUpdateType)
        message.getField(noMDEntryType)
        message.getField(noRelatedSym)

        groupMD= fix42.MarketDataRequest().NoMDEntryTypes()
        mdEntries=[]
        for MDIndex in range(noMDEntryType.getValue()):
            message.getGroup(MDIndex+1,groupMD)
            groupMD.getField(mdEntryType)
            mdEntries.append(mdEntryType.getValue())

        symbolGroup = fix42.MarketDataRequest().NoRelatedSym()
        symbols=[]
        symbol=fix.Symbol()
        for asymbol in range(noRelatedSym.getValue()):
            message.getGroup(asymbol+1,symbolGroup)
            symbolGroup.getField(symbol)
            symbols.append(symbol.getValue())

        #Encapsulate data into market data request object
        marketDataReq= MarketDataRequest(mdReqID.getValue(),subscriptionRequestType.getValue(),marketDepth.getValue()
            ,mdUpdateType.getValue(),noMDEntryType.getValue(),mdEntries,symbols)

        #Market data Object sent to server logic to be processed
        self.server_logic.process_market_data_request(marketDataReq)
        return

#return_to_gui: current_price, day_high, day_low : json_string;
#time_stamp, price, quantity : json_string; orderstuff : json

    def send_market_data_respond(self, marketData):
        """Send market data respond

            TODO @husein

            Args:
                market_data (?): ...

            Returns:
                None
            """
        message = fix.Message()
        header = message.getHeader()
#       header.setField(fix.BeginString("FIX.4.2"))
#       header.setField(fix.BodyLength())
#       header.setField(fix.SenderCompID("server"))
#       header.setField(fix.TargetCompID("client"))
        header.setField(fix.MsgType(fix.MsgType_MarketDataSnapshotFullRefresh))
        header.setField(fix.MsgSeqNum(1))
        header.setField(fix.SendingTime())

        message.setField(fix.MDReqID(marketData.get_md_req_id()))
        #message.setField(fix.SecurityType('CS'))
        #message.setField(fix.MaturityMonthYear("201712"))
        #message.setField(fix.PutOrCall('0'))
        #message.setField(fix.StrikePrice(100.00))
        message.setField(fix.NoMDEntries(marketData.get_no_md_entries()))
        message.setField(fix.Symbol(marketData.get_symbol()))
        message.setField(fix.TotalVolumeTraded(marketData.get_total_volume_traded()))

        group= fix42.MarketDataSnapshotFullRefresh.NoMDEntries()
        mdEntries= marketData.get_md_entry_type()
        mdEntryPx=marketData.get_md_entry_px()
        mdEntrySize=marketData.get_md_entry_size()
        mdEntryTime=marketData.get_md_entry_time()
        currency=marketData.get_currency()
        numberOfOrders=marketData.get_number_of_orders()
        """ Used if handling with list of symbol
        symbols= mdreq.get_symbols()
        for asymbol in range(symbols)):
            print("Symbol "+symbols[asymbol])
        """

        for MDIndex in range (marketData.get_no_md_entries()):
            group.setField(fix.MDEntryType(mdEntries[MDIndex]))
            group.setField(fix.MDEntryPx(mdEntryPx[MDIndex]))
            group.setField(fix.MDEntrySize(mdEntrySize[MDIndex]))
            #group.setField(fix.MDEntryTime(mdEntryTime[MDIndex])) not sure why cannot instantiate object with int var
            group.setField(fix.MDEntryTime())
            group.setField(fix.Currency(currency[MDIndex]))
            group.setField(fix.NumberOfOrders(numberOfOrders[MDIndex]))
            message.addGroup(group)

        fix.Session.sendToTarget(message,self.fix_application.sessionID)

        return


class ServerLogic:
    def __init__(self, server_config_file_name):
        self.server_fix_handler = ServerFIXHandler(self, server_config_file_name)
        self.server_database_handler = ServerDatabaseHandler()
        self.market_simulation_handler = MarketSimulationHandler()
        self.initialize_new_stocks = True

    def start_server(self):
        if self.initialize_new_stocks:
            self.server_database_handler.delete_all_stock_data()
            self.market_simulation_handler.init()
        self.server_fix_handler.start()
        while 1: time.sleep(1)
        self.stop_server()

    def stop_server(self):
        self.server_fix_handler.stop()

    def process_logon(self, user_id, password):
        respond = self.authenticate_user(user_id, password)
        return respond

    def process_market_data_request(self, mdreq):
        """Process market data request


		Args:
			symbols (list of str): A list of symbol tickers.

		Returns:
			bool: The return value. True for success, False otherwise.
		"""

        #Subscribe means will be sent periodically, so for now we use snapshot
        if mdreq.get_subscription_request_type() == 0:
            print("0 = Snapshot")
        elif mdreq.get_subscription_request_type() == 1:
            print("1 = Snapshot + Updates (Subscribe)")
        elif mdreq.get_subscription_request_type() == 2:
            print("2 = Disable previous Snapshot + Update Request (Unsubscribe)")

        #Now we will only support Full Refresh which is only sent with 1 symbol
        if mdreq.get_md_update_type() == 0:
            print("Full Refresh") #Return W Full Refresh/Snapshot Message
        elif mdreq.get_md_update_type() == 1:
            print("Incremental Refresh") #Return X Incremental Refresh Message

        #Now we wll only support Top of Book (only best prices quoted), Full of Book means all the traded data.
        if mdreq.get_market_depth() == 0:
            print("Full Book")
        elif mdreq.get_market_depth() == 1:
            print("Top of Book")

        mdReqID=mdreq.get_md_req_id()
        noMDEntries= mdreq.get_no_md_entry_type()
        symbol=mdreq.get_symbols(0)
        totalVolumeTraded=1000
        mdEntries= mdreq.get_md_entries()
        mdEntryPxList=[]
        mdEntrySizeList=[]
        mdEntryTimeList=[]
        currencyList=[]
        numberOfOrdersList=[]

        #Should be retrieving Market Data using Required Symbol and Parameter
        for MDIndex in range (mdreq.get_no_md_entry_type()):
            mdEntryPxList.append(100)
            mdEntrySizeList.append(5)
            mdEntryTimeList.append(time.time())
            currencyList.append("CNY"+mdEntries[MDIndex])
            numberOfOrdersList.append(9)

        #Encapsulate data into market data response object
        market_data= MarketDataResponse(mdReqID, noMDEntries, symbol, totalVolumeTraded, mdEntries, mdEntryPxList,
                                        mdEntrySizeList, mdEntryTimeList, currencyList, numberOfOrdersList)

        #Send Market Data to Fix Handler
        self.server_fix_handler.send_market_data_respond(market_data)

        pass

    def authenticate_user(self, user_id, password):
        """Authenticates user

        Checks if user with the given id and password exists in database

        Args:
            user_id (string): The user id
            password (string): The password

        Returns:
            success (ServerRespond): success of authentication
        """
        # TODO #29 add authentication
        return ServerRespond.AUTHENTICATION_SUCCESS

class ServerDatabaseHandler:
    # TODO send SQL Queries
    def __init__(self):
        pass

    def delete_all_stock_data(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='FSCDatabase', port=3306)
            cur = conn.cursor()
            execution = ("delete from Stock")
            cur.execute(execution)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    def delete_stock_data(self,stock):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='FSCDatabase', port=3306)
            cur = conn.cursor()
            execution = ("delete from Stock where Ticker = '%s' limit 1" % stock.ticker)
            cur.execute(execution)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def insert_stock_data(self, stock):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='FSCDatabase', port=3306)
            cur = conn.cursor()
            execution = ("insert into Stock(Ticker, CompanyName, CurrentPrice, CurrentVolume) values( '%s', '%s', '%s', '%s')" % (stock.ticker, stock.company_name, stock.current_price, stock.current_volume))
            cur.execute(execution)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def send_client_match_query(self):
        pass

    def send_add_bid_order_query(self, symbol, price, n_shares, bidder_id):
        # send query
        return 0

    def send_remove_bid_order_query(self, bidder_id):
        return 0

    def send_remove_bid_order_query(self, bidder_id):
        return 0

    def request_historic_data(self, timestamp):
        pass


class MarketSimulationHandler:

    def __init__(self):
        self.stock_list_file_name = "stock_list.cfg"
        self.stock_list = read_file_values(self.stock_list_file_name)

    def init(self):
        self.load_market_data_into_database()

    def load_market_data_into_database(self):
        """Loads market data for initialization

		Used for server initialization to fetch data from a finance server

		Returns:
		    None
		"""
        for stock in self.stock_list:
            share = yahoo_finance.Share(stock)
            new_stock = Stock(share.data_set["symbol"], share.data_set["Name"], share.data_set["LastTradePriceOnly"], share.data_set["Volume"])
            ServerDatabaseHandler().insert_stock_data(new_stock)


class Stock:

    def __init__(self, ticker, company_name=None, current_price=None, current_volume=None):
        self.ticker = ticker
        self.company_name = company_name
        self.current_price = current_price
        self.current_volume = current_volume

    def get_ticker(self):
        return self.ticker

    def get_company_name(self):
        return self.company_name

    def get_current_price(self):
        return self.current_price

    def get_current_volume(self):
        return self.current_volume



def read_file_values(file_name):
    """Produces a list out of a file, each line represents one value

    Args:
        file_name (string): name of the file

    Returns:
        list (string): A list of stock names
    """
    with open(file_name, 'r') as file:
        list = file.read().splitlines()
    return list
