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
from TradingClass import FixOrder
from TradingClass import OrderExecution
from TradingClass import DateFix
from TradingClass import TimeFix



class ServerRespond(Enum):
    AUTHENTICATION_FAILED = 0
    AUTHENTICATION_SUCCESS = 1


class ServerFIXApplication(fix.Application):
    exec_id=0
    order_id=0

    def __init__(self, server_fix_handler):
        self.server_fix_handler = server_fix_handler
        super(ServerFIXApplication, self).__init__()

    def onCreate(self, session_id):
        self.sessionID = session_id
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
        if msg_Type.getString() == fix.MsgType_MarketDataRequest:
            print '''IN MarketDataRequest'''
            self.server_fix_handler.handle_market_data_request(message)
        elif msg_Type.getString() == fix.MsgType_NewOrderSingle:
            print '''IN NewSingleOrder'''
            self.server_fix_handler.handle_order_request(message)

    def gen_exec_id(self):
        self.exec_id = self.exec_id+1
        return self.exec_id

    def gen_order_id(self):
        self.order_id = self.order_id+1
        return self.order_id


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
    			message (fix message): market data request message

    		Returns:
    			None
    		"""

        # Retrieving Fix Data from market data request sent by client
        md_req_id_fix = fix.MDReqID()
        subscription_request_type_fix = fix.SubscriptionRequestType()
        market_depth_fix = fix.MarketDepth()
        no_md_entry_types_fix = fix.NoMDEntryTypes()
        md_entry_type_fix = fix.MDEntryType()
        no_related_sym_fix = fix.NoRelatedSym()

        message.getField(md_req_id_fix)
        message.getField(subscription_request_type_fix)
        message.getField(market_depth_fix)
        message.getField(no_md_entry_types_fix)
        message.getField(no_related_sym_fix)

        group_md = fix42.MarketDataRequest().NoMDEntryTypes()
        md_entries = []
        for md_idx in range(no_md_entry_types_fix.getValue()):
            message.getGroup(md_idx + 1, group_md)
            group_md.getField(md_entry_type_fix)
            md_entries.append(md_entry_type_fix.getValue())

        group_symbol = fix42.MarketDataRequest().NoRelatedSym()
        symbols = []
        symbol = fix.Symbol()
        for symbol_idx in range(no_related_sym_fix.getValue()):
            message.getGroup(symbol_idx + 1, group_symbol)
            group_symbol.getField(symbol)
            symbols.append(symbol.getValue())

        # Encapsulate data into market data request object
        md_request = MarketDataRequest(md_req_id_fix.getValue(), subscription_request_type_fix.getValue()
            , market_depth_fix.getValue(),no_md_entry_types_fix.getValue(),md_entries, no_related_sym_fix.getValue()
            , symbols)

        # Market data Object sent to server logic to be processed
        self.server_logic.process_market_data_request(md_request)
        return

    # return_to_gui: current_price, day_high, day_low : json_string;
    # time_stamp, price, quantity : json_string; orderstuff : json

    def send_market_data_respond(self, market_data):
        """Send market data respond

            TODO @husein

            Args:
                market_data MarketDataResponse Object

            Returns:
                None
            """

        #Create Market Data Response Fix Message from market_data
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_MarketDataSnapshotFullRefresh))
        header.setField(fix.MsgSeqNum(1))
        header.setField(fix.SendingTime())
        message.setField(fix.MDReqID(market_data.get_md_req_id()))
        message.setField(fix.NoMDEntries(market_data.get_no_md_entry_types()))
        message.setField(fix.Symbol(market_data.get_symbol()))

        group_md_entry = fix42.MarketDataSnapshotFullRefresh.NoMDEntries()
        md_entry_type = market_data.get_md_entry_type_list()
        md_entry_px = market_data.get_md_entry_px_list()
        md_entry_size = market_data.get_md_entry_size_list()
        md_entry_date = market_data.get_md_entry_date_list()
        md_entry_time = market_data.get_md_entry_time_list()
        entry_date_fix = fix.MDEntryDate()
        entry_time_fix = fix.MDEntryTime()
        for md_index in range(market_data.get_no_md_entry_types()):
            entry_date_fix.setString(md_entry_date[md_index].__str__())
            entry_time_fix.setString(md_entry_time[md_index].__str__())
            group_md_entry.setField(fix.MDEntryType(md_entry_type[md_index]))
            group_md_entry.setField(fix.MDEntryPx(md_entry_px[md_index]))
            group_md_entry.setField(fix.MDEntrySize(md_entry_size[md_index]))
            group_md_entry.setField(entry_date_fix)
            group_md_entry.setField(entry_time_fix)
            message.addGroup(group_md_entry)

        #Send the message to client
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

        return

    def handle_order_request(self, message):
        """Process market data request
            TODO @husein

            Args:
            message :  order fix message received from client

            Returns:
            None
        """
        # Retrieving Fix Data from order request sent by client
        cl_ord_id_fix = fix.ClOrdID()
        handl_inst_fix = fix.HandlInst()
        exec_inst_fix = fix.ExecInst()
        symbol_fix = fix.Symbol()
        maturity_month_year_fix = fix.MaturityMonthYear()
        maturity_day_fix = fix.MaturityDay()
        side_fix = fix.Side()
        transact_time_fix = fix.TransactTime()
        order_qty_fix = fix.OrderQty()
        ord_type_fix = fix.OrdType()
        price_fix = fix.Price()
        stop_px_fix = fix.StopPx()

        message.getField(cl_ord_id_fix)
        message.getField(handl_inst_fix)
        message.getField(exec_inst_fix)
        message.getField(symbol_fix)
        message.getField(maturity_month_year_fix)
        message.getField(maturity_day_fix)
        message.getField(side_fix)
        message.getField(transact_time_fix)
        message.getField(order_qty_fix)
        message.getField(ord_type_fix)
        message.getField(price_fix)
        message.getField(stop_px_fix)

        #Create FixOrder Object to be sent to server logic
        fix_order= FixOrder(cl_ord_id_fix.getValue(),handl_inst_fix.getValue(),exec_inst_fix.getValue(),
        symbol_fix.getValue(), maturity_month_year_fix.getValue(), maturity_day_fix.getValue(),
        side_fix.getValue(), transact_time_fix.getString(), order_qty_fix.getValue(), ord_type_fix.getValue(),
        price_fix.getValue(), stop_px_fix.getValue())

        self.server_logic.process_order_request(fix_order)

        return

    def send_order_execution_respond(self, order_execution):
        """Send order execution respond

            TODO @husein

            Args:
                order_execution : OrderExecution object created in server logic

            Returns:
                None
            """
        #Create Execution Report Fix Message based on order_execution object created in server logic
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
        header.setField(fix.MsgSeqNum(self.fix_application.exec_id))
        header.setField(fix.SendingTime())

        message.setField(fix.OrderID(order_execution.get_order_id()))
        message.setField(fix.ClOrdID(order_execution.get_cl_ord_id()))
        message.setField(fix.ExecID(order_execution.get_exec_id()))
        message.setField(fix.ExecTransType(order_execution.get_exec_trans_type())) #0 = New,1 = Cancel,2 = Correct,3 = Status
        message.setField(fix.ExecType(order_execution.get_exec_type())) #0 = New,1 = Partially filled,2 = Filled,3 = Done for day,4 = Canceled
        message.setField(fix.OrdStatus(order_execution.get_ord_status()))#0 = New,1 = Partially filled,2 = Filled,3 = Done for day,4 = Canceled
        message.setField(fix.Symbol(order_execution.get_symbol()))
        message.setField(fix.Side(order_execution.get_side()))
        message.setField(fix.LeavesQty(order_execution.get_leaves_qty()))
        message.setField(fix.CumQty(order_execution.get_cum_qty()))
        message.setField(fix.AvgPx(order_execution.get_avg_px()))
        message.setField(fix.Price(order_execution.get_price()))
        message.setField(fix.StopPx(order_execution.get_stop_px()))

        fix.Session.sendToTarget(message, self.fix_application.sessionID)
        return

class ServerLogic:
    def __init__(self, server_config_file_name):
        self.server_fix_handler = ServerFIXHandler(self, server_config_file_name)
        self.server_database_handler = ServerDatabaseHandler()
        self.market_simulation_handler = MarketSimulationHandler()
        self.initialize_new_database = True

    def start_server(self):
        if self.initialize_new_database:
            self.server_database_handler.create_database()
            self.market_simulation_handler.init_market()
        self.server_fix_handler.start()
        while 1: time.sleep(1)
        self.stop_server()

    def stop_server(self):
        self.server_fix_handler.stop()

    def process_logon(self, user_id, password):
        respond = self.authenticate_user(user_id, password)
        return respond

    def process_market_data_request(self, md_request):
        """Process market data request

		Args:
			md_request : MarketDataRequest Object

		Returns:
			bool: The return value. True for success, False otherwise.
		"""

        # Subscribe means will be sent periodically, so for now we use snapshot
        if md_request.get_subscription_request_type() == 0:
            print("0 = Snapshot")
        elif md_request.get_subscription_request_type() == 1:
            print("1 = Snapshot + Updates (Subscribe)")
        elif md_request.get_subscription_request_type() == 2:
            print("2 = Disable previous Snapshot + Update Request (Un-subscribe)")

        # Now we wll only support Top of Book (only best prices quoted), Full of Book means all the traded data.
        if md_request.get_market_depth() == 0:
            print("Full Book")
        elif md_request.get_market_depth() == 1:
            print("Top of Book")

        md_req_id = md_request.get_md_req_id()
        no_md_entries = md_request.get_no_md_entry_types()
        symbol = md_request.get_symbol(0)
        md_entry_type_list = md_request.get_md_entry_type_list()
        md_entry_px_list = []
        md_entry_size_list = []
        md_entry_date_list = []
        md_entry_time_list = []

        # Should be retrieving Market Data using Required Symbol and Parameter
        a_date= DateFix(2013,2,1)
        a_date.set_date_string("20140201")
        a_time= TimeFix(10,1,0)
        a_time.set_time_string("10:02:00")
        for MDIndex in range(md_request.get_no_md_entry_types()):
            md_entry_px_list.append(100)
            md_entry_size_list.append(5)
            md_entry_date_list.append(a_date)
            md_entry_time_list.append(a_time)

        # Encapsulate data into market data response object
        market_data = MarketDataResponse(md_req_id, no_md_entries, symbol, md_entry_type_list, md_entry_px_list,
                                         md_entry_size_list, md_entry_date_list, md_entry_time_list)

        # Send Market Data to Fix Handler
        self.server_fix_handler.send_market_data_respond(market_data)

        pass

    def process_order_request(self, fix_order):
        """Process an order request from the FIX Handler


        Args:
            fix_order (FixOrder): FixOrder Object from fix handler

        Returns:
            None
        """

        #Handling fix_order object from the fix message
        print(fix_order.get_cl_ord_id())
        print(fix_order.get_handl_inst())
        print(fix_order.get_exec_inst())
        print(fix_order.get_symbol())
        print(fix_order.get_maturity_month_year())
        print(fix_order.get_maturity_day())
        print(fix_order.get_side())
        print(fix_order.get_transact_time())
        print(fix_order.get_order_qty())
        print(fix_order.get_ord_type())
        print(fix_order.get_price())
        print(fix_order.get_stop_px())

        #TODO this is only outline, does not work
        """ Doing Matching Algorithm and insert database
        order= None
        self.server_database_handler.insert_order(order)
        stock = None
        # stock = Stock(Order.stock_ticker)
        buy_orders, sell_orders = self.server_database_handler.request_orders_for_stock(stock)
        matching_matrix = self.matching_algorithm.match_orders(buy_orders, sell_orders)
        # inform each client being matched
        self.resolve_matching_matrix(matching_matrix)
        """
        #Retrieve the database and process related order

        #Create Order Execution report value based on processed order
        order_id= str(self.server_fix_handler.fix_application.gen_order_id())
        cl_ord_id=fix_order.get_cl_ord_id()
        exec_id=str(self.server_fix_handler.fix_application.gen_exec_id())
        exec_trans_type='0'
        exec_type='2'
        ord_status='2'
        symbol=fix_order.get_symbol()
        side=fix_order.get_side()
        leaves_qty=0
        cum_qty=200
        avg_px=999
        price=900
        stop_px=1000

        #Encapsulate result of processing into execution report
        order_execution= OrderExecution(order_id, cl_ord_id, exec_id, exec_trans_type, exec_type, ord_status
            , symbol, side, leaves_qty, cum_qty, avg_px, price, stop_px)

        #Send Order Execution object to server fix handler
        self.server_fix_handler.send_order_execution_respond(order_execution)

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
        self.user_name = "root"
        self.user_password = "123456" #
        self.database_name = "FSCDatabase"
        self.database_port = 3306
        self.database_creation_file_path = "./database/server_database.sql"

    def create_database(self):
        self.load_sql_file(self.database_creation_file_path)

    def load_sql_file(self, file_path):
        sql_commands = read_file(file_path).split(";")
        for sql_command in sql_commands:
            self.execute_sql_command(sql_command)

    def execute_sql_command(self, sql_command):
        try:
            conn = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                   db=self.database_name, port=self.database_port)
            cur = conn.cursor()
            execution = (sql_command)
            cur.execute(execution)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    def delete_all_stock_data(self):
        command = "delete from Stock"
        self.execute_sql_command(command)

    def delete_stock_data(self, stock):
        command = ("delete from Stock where Ticker = '%s' limit 1" % stock.ticker)
        self.execute_sql_command(command)

    def insert_stock_data(self, stock):
        command = (
                "insert into Stock(Ticker, CompanyName, LotSize, TickSize, TotalVolume) values( '%s', '%s', '%s', '%s')" % (
                stock.get_ticker, stock.get_company_name, stock.get_lot_size(), stock.get_tick_size(),
                stock.get_total_volume()))
        self.execute_sql_command(command)

    def fetch_stock(self, stock):
        pass

    def fetch_stock_information(self, stock):
        pass

    def request_orders_of_type(self, order):
        """Returns all orders for the same stock as the given order


        Args:
            order (string): The user id
            password (string): The password

        Returns:
            success (ServerRespond): success of authentication
        """

    def request_orders_for_stock(self, stock):
        """Returns all orders for the same stock as the given order


        Args:
            stock (Stock): The stock for which the orders are searched for

        Returns:
            buy_orders (list<Order>): list of buying orders for the stock
            sell_orders (list<Order>): list of selling orders for the stock
        """

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

    def init_market(self):
        ServerDatabaseHandler().load_sql_file("./database/stock_data_insert.sql")
        #self.load_market_data_into_database()

    def load_market_data_into_database(self):
        """Loads market data for initialization

		Used for server initialization to fetch data from a finance server

		Returns:
		    None
		"""
        for stock in self.stock_list:
            share = yahoo_finance.Share(stock)
            new_stock = Stock(share.data_set["symbol"], share.data_set["Name"], share.data_set["LastTradePriceOnly"],
                              share.data_set["Volume"])
            ServerDatabaseHandler().insert_stock_data(new_stock)


class Stock:
    def __init__(self, ticker, company_name=None, lot_size=None, tick_size=None, total_volume=None):
        self.ticker = ticker
        self.company_name = company_name
        self.lot_size = lot_size
        self.tick_size = tick_size
        self.total_volume = total_volume

    def get_ticker(self):
        return self.ticker

    def get_company_name(self):
        return self.company_name

    def get_lot_size(self):
        return self.lot_size

    def get_tick_size(self):
        return self.tick_size

    def get_total_volume(self):
        return self.total_volume

def read_file(file_name):
    """Produces a string without \n

    Args:
        file_name (string): name of the file

    Returns:
        list (string): A list of stock names
    """
    with open(file_name, 'r') as file:
        content = file.read()
    return content


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
