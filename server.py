import quickfix as fix
import sys
import time
import pdb
from enum import Enum





class Message():
    def __init__(self, code, description):
        self.code = code
        self.description = description



class ServerRespond(Enum):
    REJECT_LOGON_REQUEST = 0

class ServerLogicRespond(Enum):
    AUTHENTICATION_SUCCESS = 0
    AUTHENTICATION_FAILED_WRONG_USER_PASSWORD = 1

class DatabaseRespond(Enum):
    SUCCESS = 0
    FAILURE = 1




class ServerFIXHandler(fix.Application):
    orderID = 0
    execID = 0

    # TODO FIX COMMUNICATION
    def onCreate(self, session_id):
        self.server_logic = ServerLogic()
        return

    def onLogon(self, session_id):
        return

    def onLogout(self, session_id):
        return

    def toAdmin(self, message, session_id):
        return

    def fromAdmin(self, message, session_id):
        """React to admin level messages

        When a message is received on admin level like Logon or Logout,
        this function is invoked with the message
        TODO are there any other admin messages which are relevant for us?

        Args:
            message (Swig Object of type 'FIX::Message *'): The received message
            session_id (Swig Object of type 'FIX::SessionID *'): The received message

        Returns:
            nothing
        """

        begin_string = message.getHeader().getField(fix.BeginString())  # returns 'FIX::FieldBase *'
        msg_type = message.getHeader().getField(fix.MsgType())

        if msg_type.getString() == fix.MsgType_Logon:
            self.__handle_logon_request(message, session_id)
        else:
            #TODO send error: MsgType not understand
            pass

        return

    def toApp(self, message, session_id):
        return

    def fromApp(self, message, session_id):
        """React to admin level messages

        When a message is received on application level like ...,
        this function is invoked with the message
        TODO what kind of messages go through here?

        Args:
            message (Swig Object of type 'FIX::Message *'): The received message
            session_id (Swig Object of type 'FIX::SessionID *'): The received message

        Returns:
            nothing
        """
        # msgType = fix.MsgType()
        print("Received message")
        # contains FIX version
        beginString = message.getHeader().getField(fix.BeginString())
        msgType = message.getHeader().getField(fix.MsgType())

        # contains basic information of message
        symbol = fix.Symbol()
        side = fix.Side()
        ordType = fix.OrdType()
        orderQty = fix.OrderQty()
        price = fix.Price()
        clOrdID = fix.ClOrdID()

        # check if msgType is valid
        message.getField(ordType)
        if ordType.getValue() != fix.OrdType_LIMIT:
            raise fix.IncorrectTagValue(ordType.getField())

        # get basic information of message
        message.getField(symbol)
        message.getField(side)
        message.getField(orderQty)
        message.getField(price)
        message.getField(clOrdID)

        executionReport = fix.Message()
        executionReport.getHeader().setField(beginString)
        executionReport.getHeader().setField(fix.MsgType(fix.MsgType_ExecutionReport))

        executionReport.setField(fix.OrderID(self.genOrderID()))
        executionReport.setField(fix.ExecID(self.genExecID()))
        executionReport.setField(fix.OrdStatus(fix.OrdStatus_FILLED))
        executionReport.setField(symbol)
        executionReport.setField(side)
        executionReport.setField(fix.CumQty(orderQty.getValue()))
        executionReport.setField(fix.AvgPx(price.getValue()))
        executionReport.setField(fix.LastShares(orderQty.getValue()))
        executionReport.setField(fix.LastPx(price.getValue()))
        executionReport.setField(clOrdID)
        executionReport.setField(orderQty)

        if beginString.getValue() == fix.BeginString_FIX40 or beginString.getValue() == fix.BeginString_FIX41 or beginString.getValue() == fix.BeginString_FIX42:
            executionReport.setField(fix.ExecTransType(fix.ExecTransType_NEW))

        if beginString.getValue() >= fix.BeginString_FIX41:
            executionReport.setField(fix.ExecType(fix.ExecType_FILL))
            executionReport.setField(fix.LeavesQty(0))

        try:
            fix.Session.sendToTarget(executionReport, session_id)
        except fix.SessionNotFound as e:
            return

    def __handle_logon_request(self, message, session_id):
        are_all_fields_set, missing_field = self.__are_all_fields_set(message, fix.RawData(), fix.SenderSubID())
        if not are_all_fields_set:
            respond = Message(ServerRespond.REJECT_LOGON_REQUEST, missing_field.__class__.__name__+" field is missing")
            self.__send_reject_message(respond, session_id)
        password = message.getField(fix.RawData())
        user_id = message.getField(fix.SenderSubID())
        logon_respond = self.server_logic.authenticate_user(user_id, password)
        if logon_respond == ServerLogicRespond.AUTHENTICATION_FAILED_WRONG_USER_PASSWORD:
            # TODO reject client AUTHENTICATION_FAILED_WRONG_USER_PASSWORD
            pass

        return

    def __send_reject_message(self, respond, session_id):
        pass


    def __unpack_logon_request(self, username, password, timestamp):
        pass

    def __unpack_logout_request(self, username, password, timestamp):
        pass

    def __unpack_execution_report(self):
        pass

    def __unpack_order_request(self, symbol, n_shares):
        pass

    def __unpack_order_cancel_request(self):
        pass

    def __unpack_market_data_request(self):
        """Process market data request

		Used for server initialization to fetch data

		Args:
			symbols (list of str): A list of symbol tickers.

		Returns:
			bool: The return value. True for success, False otherwise.
		"""
        pass

    def __pack_order_status_request(self):
        pass

    def __pack_market_data_reply(self):
        pass

    # To use for the server
    def send_order_status_request(self, sessionID):
        message = self.__pack_order_status_request()
        self.__send_message(message, sessionID)
        pass

    def send_market_data_reply(self, sessionID):
        message = self.__pack_market_data_reply()
        self.__send_message(message, sessionID)
        pass

    def __are_all_fields_set(self, message, *fields):
        """Process market data request

        Used for server initialization to fetch data

        Args:
            fields (objects): fix fields like fix.MsgType

        Returns:
            int: if a field is missing
            object: first fix fields which is missing
        """
        pass
        for i in range(len(fields)):
            if not message.isSetField(fields[i]):
                return 0, fields[i]
        return 1, None




class ServerLogic:
    def __init__(self):
        pass

    def authenticate_user(self, user_id, password):
        """Authenticates user

        Checks if user is in database

        Args:
            message (Swig Object of type 'FIX::Message *'): The received message
            session_id (Swig Object of type 'FIX::SessionID *'): The received message

        Returns:
            nothing
        """
        # TODO #29 add authentication
        return ServerLogicRespond.AUTHENTICATION_SUCCESS

    def process_logon_request(self, username, password, timestamp):
        pass

    def process_logout_request(self, username, password, timestamp):
        pass

    def process_execution_report(self):
        pass

    def process_order_request(self, symbol, n_shares):
        pass

    def process_order_cancel_request(self):
        pass

    def process_market_data_request(self, symbols):
        """Process market data request

		Used for server initialization to fetch data

		Args:
			symbols (list of str): A list of symbol tickers.

		Returns:
			bool: The return value. True for success, False otherwise.
		"""
        pass

    def __match_orders(self):
        """Process market data request

        Used for server initialization to fetch data

        Args:
            symbols (list of str): A list of symbol tickers.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        pass


class ServerDatabaseHandler:
    # TODO send SQL Queries
    def send_client_match_query(self):
        pass

    def send_add_bid_order_query(self, symbol, price, n_shares, bidder_id):
        # send query
        return DatabaseRespond.SUCCESS

    def send_remove_bid_order_query(self, bidder_id):
        return DatabaseRespond.SUCCESS

    def send_remove_bid_order_query(self, bidder_id):
        return DatabaseRespond.SUCCESS

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
    settings = fix.SessionSettings(file)
    application = ServerFIXHandler()
    storeFactory = fix.FileStoreFactory(settings)
    # logFactory = fix.FileLogFactory(settings)
    logFactory = fix.ScreenLogFactory(settings)
    acceptor = fix.SocketAcceptor(application, storeFactory, settings, logFactory)
    acceptor.start()
    while 1: time.sleep(1)
# acceptor.stop()
except fix.ConfigError, e:
    print e
