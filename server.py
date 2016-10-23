import quickfix as fix
import quickfix42 as fix42
import sys
import time
import pdb
from enum import Enum


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
        if(msg_Type.getString() ==fix.MsgType_MarketDataRequest):
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

        print("MDReqID "+mdReqID.getValue())
        print(noMDEntryType.getValue())

        groupMD= fix42.MarketDataRequest().NoMDEntryTypes()
        mdEntryArray=[]
        for MDIndex in range(noMDEntryType.getValue()):
            message.getGroup(MDIndex+1,groupMD)
            groupMD.getField(mdEntryType)
            mdEntryArray.append(mdEntryType.getValue())

        symbolGroup = fix42.MarketDataRequest().NoRelatedSym()
        symbolArray=[]
        symbol=fix.Symbol()
        for asymbol in range(noRelatedSym.getValue()):
            message.getGroup(asymbol+1,symbolGroup)
            symbolGroup.getField(symbol)
            symbolArray.append(symbol.getValue())
            print("Symbol "+symbol.getValue())

        #Subscribe means will be sent periodically, so for now we use snapshot
        if subscriptionRequestType.getValue() == 0:
            print("0 = Snapshot")
        elif subscriptionRequestType.getValue() == 1:
            print("1 = Snapshot + Updates (Subscribe)")
        elif subscriptionRequestType.getValue() == 2:
            print("2 = Disable previous Snapshot + Update Request (Unsubscribe)")

        #Now we will only support Full Refresh which is only sent with 1 symbol
        if mdUpdateType.getValue() == 0:
            print("Full Refresh") #Return W Full Refresh/Snapshot Message
        elif mdUpdateType.getValue() == 1:
            print("Incremental Refresh") #Return X Incremental Refresh Message

        #Now we wll only support Top of Book (only best prices quoted), Full of Book means all the traded data.
        if marketDepth.getValue() == 0:
            print("Full Book")
        elif marketDepth.getValue() == 1:
            print("Top of Book")


        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.BodyLength())
        header.setField(fix.MsgType(fix.MsgType_MarketDataSnapshotFullRefresh))
        header.setField(fix.SenderCompID("server"))
        header.setField(fix.TargetCompID("client"))
        header.setField(fix.MsgSeqNum(1))
        header.setField(fix.SendingTime())

        message.setField(fix.MDReqID('1'))
        #message.setField(fix.SecurityType('CS'))
        #message.setField(fix.MaturityMonthYear("201712"))
        #message.setField(fix.PutOrCall('0'))
        #message.setField(fix.StrikePrice(100.00))
        message.setField(fix.NoMDEntries(noMDEntryType.getValue()))
        message.setField(fix.Symbol("symbol"))
        message.setField(fix.TotalVolumeTraded(1000))

        group= fix42.MarketDataSnapshotFullRefresh.NoMDEntries()

        for MDIndex in range (noMDEntryType.getValue()):
            group.setField(fix.MDEntryType(mdEntryArray[MDIndex]))
            group.setField(fix.MDEntryPx(100))
            group.setField(fix.MDEntrySize(5))
            group.setField(fix.MDEntryTime())
            group.setField(fix.Currency("CNY"+mdEntryArray[MDIndex]))
            group.setField(fix.NumberOfOrders(20))
            message.addGroup(group)

        fix.Session.sendToTarget(message,self.fix_application.sessionID)

        #Retrieve Market Data using Required Symbol and Parameter
        #Return also MDReqID, Symbol
        return

#return_to_gui: current_price, day_high, day_low : json_string;
#time_stamp, price, quantity : json_string; orderstuff : json

    def send_market_data_respond(self, market_data):
        """Send market data respond

            TODO @husein

            Args:
                market_data (?): ...

            Returns:
                None
            """
        return


class ServerLogic:
    def __init__(self, server_config_file_name):
        self.server_fix_handler = ServerFIXHandler(self, server_config_file_name)
        self.server_database_handler = ServerDatabaseHandler()
        self.market_simulation_handler = MarketSimulationHandler()

    def start_server(self):
        self.server_fix_handler.start()
        while 1: time.sleep(1)
        self.stop_server()

    def stop_server(self):
        self.server_fix_handler.stop()

    def process_logon(self, user_id, password):
        respond = self.authenticate_user(user_id, password)
        return respond

    def process_market_data_request(self, symbols):
        """Process market data request


		Args:
			symbols (list of str): A list of symbol tickers.

		Returns:
			bool: The return value. True for success, False otherwise.
		"""
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
    stock_market = "NYSE"

    # TODO
    def request_market_data(self, symbols):
        """Request market data for initialization

		Used for server initialization to fetch data

		Args:
		    symbols (list of str): A list of symbol tickers.

		Returns:
		    bool: The return value. True for success, False otherwise.
		"""
        pass


try:
    file = sys.argv[1] if len(sys.argv) == 2 else "server.cfg"
    server = ServerLogic(file)
    server.start_server()
except fix.ConfigError, e:
    print e
