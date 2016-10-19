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


class ServerFIXApplication(fix.Application):
    def __init__(self, server_fix_handler):
        self.server_fix_handler = server_fix_handler
        super(ServerFIXApplication, self).__init__()

    def onCreate(self, session_id):
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

        #begin_string = message.getHeader().getField(fix.BeginString())  # returns 'FIX::FieldBase *'
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
        #TODO
        # msgType = fix.MsgType()
        print("Received message")
        # contains FIX version
        beginString = message.getHeader().getField(fix.BeginString())
        msgType = message.getHeader().getField(fix.MsgType())


class ServerFIXHandler():
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
        self.application = ServerFIXApplication(self)
        storeFactory = fix.FileStoreFactory(settings)
        # logFactory = fix.FileLogFactory(settings)
        logFactory = fix.ScreenLogFactory(settings)
        self.socket_acceptor = fix.SocketAcceptor(self.application, storeFactory, settings, logFactory)

    def handle_logon_request(self, message):
        password = message.getField(fix.RawData())
        user_id = message.getHeader().getField(fix.SenderSubID())
        print "\n"+user_id.getString() + "\n"
        print password.getString()+"\n"
        logon_respond = self.server_logic.authenticate_user(user_id, password)
        if logon_respond == ServerLogicRespond.AUTHENTICATION_FAILED_WRONG_USER_PASSWORD:
            # TODO reject client AUTHENTICATION_FAILED_WRONG_USER_PASSWORD
            pass

        return

    def send_reject_message(self, respond, session_id):
        pass

    def unpack_logon_request(self, username, password, timestamp):
        pass

    def unpack_logout_request(self, username, password, timestamp):
        pass

    def unpack_execution_report(self):
        pass

    def unpack_order_request(self, symbol, n_shares):
        pass

    def unpack_order_cancel_request(self):
        pass

    def unpack_market_data_request(self):
        """Process market data request

		Used for server initialization to fetch data

		Args:
			symbols (list of str): A list of symbol tickers.

		Returns:
			bool: The return value. True for success, False otherwise.
		"""
        pass

    def pack_order_status_request(self):
        pass

    def pack_market_data_reply(self):
        pass

    # To use for the server
    def send_order_status_request(self, sessionID):
        message = self.pack_order_status_request()
        self.send_message(message, sessionID)
        pass

    def send_market_data_reply(self, sessionID):
        message = self.__pack_market_data_reply()
        self.send_message(message, sessionID)
        pass


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

    def authenticate_user(self, user_id, password):
        """Authenticates user

        Checks if user with the given id and password exists in database

        Args:
            user_id (string): The user id
            password (string): The password

        Returns:
            if
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
    def __init__(self):
        pass

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
    server = ServerLogic(file)
    server.start_server()
except fix.ConfigError, e:
    print e
