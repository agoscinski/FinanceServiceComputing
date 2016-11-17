from tarfile import _section
import quickfix as fix
import quickfix42 as fix42
import sys
import time
import datetime
import yahoo_finance
import MySQLdb
from enum import Enum
import matching_algorithm
import TradingClass
from TradingClass import MarketDataRequest
from TradingClass import MarketDataResponse
from TradingClass import FIXOrder
from TradingClass import Order
from TradingClass import OrderExecution
from TradingClass import FIXDate
from TradingClass import FIXTime


class ServerRespond(Enum):
    AUTHENTICATION_FAILED = 0
    AUTHENTICATION_SUCCESS = 1


class ServerFIXApplication(fix.Application):
    exec_id = 0
    order_id = 0

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
        self.exec_id = self.exec_id + 1
        return self.exec_id

    def gen_order_id(self):
        self.order_id = self.order_id + 1
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
        self.logFactory = fix.FileLogFactory(settings)
        # self.logFactory = fix.ScreenLogFactory(settings)
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
            md_entries.append(int(md_entry_type_fix.getValue()))

        group_symbol = fix42.MarketDataRequest().NoRelatedSym()
        symbols = []
        symbol = fix.Symbol()
        for symbol_idx in range(no_related_sym_fix.getValue()):
            message.getGroup(symbol_idx + 1, group_symbol)
            group_symbol.getField(symbol)
            symbols.append(symbol.getValue())

        # Encapsulate data into market data request object
        md_request = MarketDataRequest(md_req_id_fix.getValue(), subscription_request_type_fix.getValue()
                                       , market_depth_fix.getValue(), no_md_entry_types_fix.getValue(), md_entries,
                                       no_related_sym_fix.getValue()
                                       , symbols)

        # Market data Object sent to server logic to be processed
        self.server_logic.process_market_data_request(md_request)
        return

    # return_to_gui: current_price, day_high, day_low : json_string;
    # time_stamp, price, quantity : json_string; orderstuff : json

    def send_market_data_respond(self, market_data):
        """Send market data respond

            Args:
                market_data MarketDataResponse Object

            Returns:
                None
            """

        # Create Market Data Response Fix Message from market_data
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
            # TODO time should not be here i think
            # entry_time_fix.setString(md_entry_time[md_index].__str__())
            group_md_entry.setField(fix.MDEntryType(md_entry_type[md_index]))
            group_md_entry.setField(fix.MDEntryPx(md_entry_px[md_index]))
            group_md_entry.setField(fix.MDEntrySize(md_entry_size[md_index]))
            group_md_entry.setField(entry_date_fix)
            group_md_entry.setField(entry_time_fix)
            message.addGroup(group_md_entry)

        # Send the message to client
        fix.Session.sendToTarget(message, self.fix_application.sessionID)

        return

    def handle_order_request(self, message):
        """Process market data request

            Args:
            message :  order fix message received from client

            Returns:
            None
        """
        # Retrieving Fix Data from order request sent by client
        header = message.getHeader()
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
        sender_comp_id = self.get_header_field_value(fix.SenderCompID(), message)
        sending_time = self.get_header_field_string(fix.SendingTime(), message)
        on_behalf_of_comp_id = self.get_header_field_value(fix.OnBehalfOfCompID(), message)
        sender_sub_id = self.get_header_field_value(fix.SenderSubID(), message)

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

        # Create FixOrder Object to be sent to server logic
        fix_order = FIXOrder(cl_ord_id_fix.getValue(), handl_inst_fix.getValue(), exec_inst_fix.getValue(),
                             symbol_fix.getValue(), maturity_month_year_fix.getValue(), maturity_day_fix.getValue(),
                             side_fix.getValue(), transact_time_fix.getString(), order_qty_fix.getValue(),
                             ord_type_fix.getValue(),
                             price_fix.getValue(), stop_px_fix.getValue(), sender_comp_id, sending_time,
                             on_behalf_of_comp_id, sender_sub_id)

        self.server_logic.process_order_request(fix_order)

        return

    def send_order_execution_respond(self, order_execution):
        """Send order execution respond

            Args:
                order_execution : OrderExecution object created in server logic

            Returns:
                None
            """
        # Create Execution Report Fix Message based on order_execution object created in server logic
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
        header.setField(fix.MsgSeqNum(self.fix_application.exec_id))
        header.setField(fix.SendingTime())

        message.setField(fix.OrderID(order_execution.get_order_id()))
        message.setField(fix.ClOrdID(order_execution.get_cl_ord_id()))
        message.setField(fix.ExecID(order_execution.get_exec_id()))
        message.setField(
            fix.ExecTransType(order_execution.get_exec_trans_type()))  # 0 = New,1 = Cancel,2 = Correct,3 = Status
        message.setField(fix.ExecType(
            order_execution.get_exec_type()))  # 0 = New,1 = Partially filled,2 = Filled,3 = Done for day,4 = Canceled
        message.setField(fix.OrdStatus(
            order_execution.get_ord_status()))  # 0 = New,1 = Partially filled,2 = Filled,3 = Done for day,4 = Canceled
        message.setField(fix.Symbol(order_execution.get_symbol()))
        message.setField(fix.Side(order_execution.get_side()))
        message.setField(fix.LeavesQty(order_execution.get_leaves_qty()))
        message.setField(fix.CumQty(order_execution.get_cum_qty()))
        message.setField(fix.AvgPx(order_execution.get_avg_px()))
        message.setField(fix.Price(order_execution.get_price()))
        message.setField(fix.StopPx(order_execution.get_stop_px()))

        fix.Session.sendToTarget(message, self.fix_application.sessionID)
        return

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


def transform_fix_order_to_order(fix_order):
    #TODO move to TradingClass.Order.create_from_new_single_order()
    """Process an order request from the FIX Handler

    Args:
        fix_order (TradingClass.FIXOrder): FixOrder Object from fix handler

    Returns:
        order (TradingClass.Order): The order object
    """

    # Subscribe means will be sent periodically, so for now we use snapshot

    account_company_id = fix_order.get_sender_comp_id()
    received_time = TradingClass.FIXDateTimeUTC.create_for_current_time()
    last_status = 0
    msg_seq_num = 0
    on_behalf_of_comp_id = fix_order.get_on_behalf_of_comp_id()
    sender_sub_id = fix_order.get_sender_sub_id()
    cash_order_quantity = None

    order = TradingClass.Order(fix_order.get_cl_ord_id(), account_company_id, received_time,
                               fix_order.get_handl_inst(),
                               fix_order.get_symbol(), fix_order.get_side(),
                               fix_order.get_ord_type(), fix_order.get_order_qty(),
                               fix_order.get_price(), last_status, msg_seq_num, on_behalf_of_comp_id,
                                sender_sub_id,
                                cash_order_quantity)
    fix.Order()
    return order


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
        md_entry_type_list = md_request.md_entry_type_list

        pending_stock_orders = self.server_database_handler.fetch_pending_orders_for_stock_ticker(symbol)
        stock_information = self.server_database_handler.fetch_stock_information(symbol)
        market_data_response = self.pack_into_fix_market_data_response(md_req_id, md_entry_type_list, symbol,
                                                                       pending_stock_orders, stock_information)

        self.server_fix_handler.send_market_data_respond(market_data_response)

        pass

    def process_order_request(self, requested_fix_order):
        """Process an order request from the FIX Handler

        Args:
            requested_fix_order (FIXOrder): FixOrder Object from fix handler

        Returns:
            None
        """

        requested_order = TradingClass.Order.from_new_single_order(requested_fix_order)
        order_is_valid = self.check_if_order_is_valid(requested_order)
        if order_is_valid:
            self.process_valid_order_request(requested_order)
        else:
            self.process_invalid_order_request(requested_order)


    def process_valid_order_request(self, requested_order):
        """
        Args:
            requested_order (TradingClass.Order)
        """
        self.server_database_handler.insert_order(requested_order)
        #TODO send ACK MsgType 8
        orders = self.server_database_handler.fetch_pending_orders_for_stock_ticker(requested_order.stock_ticker)
        order_executions = matching_algorithm.match(orders)
        for order_execution in order_executions:
            inserted_processed_order = self.server_database_handler.insert_order_execution(order_execution)
            self.server_fix_handler.send_order_execution_respond(inserted_processed_order)

        return None

    def process_invalid_order_request(self, requested_order):
        #TODO Husein
        pass

    def check_if_order_is_valid(self, requested_order):
        #TODO Husein
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

    def pack_into_fix_market_data_response(self, market_data_required_id, market_data_entry_types, symbol,
                                           pending_stock_orders, stock_information):
        """
        Args
            pending_stock_orders (list of TradingClass.Order)
            stock_information (TradingClass.DatabaseStockInformation)
            market_data_entry_types (list of strings): the types of orders which should be included
        Returns:

        """
        market_data_entry_type_list = []
        market_data_entry_price_list = []
        market_data_entry_size_list = []
        market_data_entry_date_list = []
        market_date_entry_time_list = []

        for pending_order in pending_stock_orders:
            #TODO make this more beautiful
            order_entry_type = 0
            if pending_order.side == 1:
                order_entry_type = 0
            elif pending_order.side == 2:
                order_entry_type = 1

            if order_entry_type in market_data_entry_types:
                #TODO show how with property this can be done better
                pending_order_date_time = pending_order.received_date.date
                pending_order_fix_date = TradingClass.FIXDate.from_year_month_day(pending_order_date_time.year,
                                                              pending_order_date_time.month,
                                                              pending_order_date_time.day)
                # TODO there should be not time anymore isn it?
                # pending_order_fix_time = TradingClass.TimeFix(pending_order_date_time.hour, pending_order_date_time.minute,
                #                                           pending_order_date_time.second)

                market_data_entry_type_list.append(order_entry_type)
                market_data_entry_price_list.append(pending_order.price)
                market_data_entry_size_list.append(pending_order.order_quantity)
                market_data_entry_date_list.append(pending_order_fix_date)
                # market_date_entry_time_list.append(pending_order_fix_time)

        current_date_time = datetime.datetime.now()
        current_fix_date = TradingClass.FIXDate.from_year_month_day(current_date_time.year, current_date_time.month,
                                                current_date_time.day)
        current_fix_time = TradingClass.FIXTime(current_date_time.hour, current_date_time.minute,
                                                current_date_time.second)
        if TradingClass.MarketDataEntryType.TRADE in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MarketDataEntryType.TRADE)
            market_data_entry_price_list.append(stock_information.current_price)
            market_data_entry_size_list.append(0)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        # TODO
        # if TradingClass.MarketDataEntryType.OPENING in market_data_entry_types_integer:

        # if 5 in market_data_entry_types_integer:
        # if 7 in market_data_entry_types_integer:
        # if 8 in market_data_entry_types_integer:

        market_data = MarketDataResponse(market_data_required_id, len(market_data_entry_type_list), symbol,
                                         market_data_entry_type_list, market_data_entry_price_list,
                                         market_data_entry_size_list, market_data_entry_date_list,
                                         market_date_entry_time_list,
                                         stock_information.current_volume)
        return market_data


class ServerDatabaseHandler:
    # TODO send SQL Queries
    def __init__(self):
        self.user_name = "root"
        self.user_password = "root"  #
        self.database_name = "FSCDatabase"
        self.database_port = 3306
        self.create_table_path = "./database/create_table.sql"

    def create_database(self):
        # load the init_script.sql file with mysql
        pass
        # self.execute_nonresponsive_sql_command("DROP SCHEMA IF EXISTS `"+self.database_name+"`", database_name="")
        # self.execute_nonresponsive_sql_command("CREATE SCHEMA IF NOT EXISTS `"+self.database_name+"` DEFAULT CHARACTER SET utf8", database_name="")
        # self.load_sql_file(self.create_table_path, database_name = "")
        # self.load_sql_file("./database/view.sql")

    def load_sql_file(self, file_path, database_name=None):
        sql_commands = read_file(file_path).split(";")
        for sql_command in sql_commands:
            self.execute_nonresponsive_sql_command(sql_command, database_name=database_name)

    def execute_nonresponsive_sql_command(self, sql_command, database_name=None):
        database_name = self.database_name if database_name is None else database_name
        try:
            conn = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                   db=database_name, port=self.database_port)
            cur = conn.cursor()
            execution = (sql_command)
            cur.execute(execution)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def insert_order_execution(self, order_execution):
        """Inserts an order execution and returns this order execution with an added execution ID

        Args:
            order_execution (TradingClass.OrderExecution): The order execution to be inserted

        Returns:
            inserted_order_execution (TradingClass.OrderExecution): The order execution which have been inserted
                and have now and execution ID
        """
        #TODO T1
        return None

    def insert_order(self, order):
        """Inserts orders of type

        Checks if user with the given id and password exists in database

        Args:
            order (TradingClass.Order): The order to be inserted

        Returns:
            None
        """
        command = (
            "INSERT INTO `Order`(ClientOrderID,Account_CompanyID, ReceivedDate, HandlingInstruction, Stock_Ticker,"
            "Side, OrderType, OrderQuantity, Price, LastStatus, MsgSeqNum) VALUES('%s','%s','%s','%s','%s','%s',"
            "'%s','%s','%s','%s','%s')"
            % (order.get_client_order_id(), order.get_account_company_id(),
               order.get_received_time().get_date_time().__str__(),
               order.get_handling_instruction(), order.get_stock_ticker(), order.get_side(), order.get_order_type(),
               order.get_order_quantity(), order.get_price(), order.get_last_status(), order.get_msg_seq_num()))
        self.execute_nonresponsive_sql_command(command)
        return

    def execute_responsive_sql_command(self, sql_command):
        fetched_database_rows = []
        try:
            conn = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                   db=self.database_name, port=self.database_port)
            cur = conn.cursor()
            execution = (sql_command)
            cur.execute(execution)
            fetched_database_rows = cur.fetchall()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        return fetched_database_rows

    def fetch_pending_orders_for_stock_ticker(self, symbol):
        """Fetches all orders from the database with status not finished

        Args:
            ticker_symbol (string): The ticker symbol for which orders are fetched

        Returns:
            order (list of TradingClass.Order): pending orders
        """

        sql_command = ("select ClientOrderID,Account_CompanyID, ReceivedDate, HandlingInstruction, Stock_Ticker,"
                       "Side, OrderType, OrderQuantity, Price, LastStatus, MsgSeqNum, OnBehalfOfCompanyID, SenderSubID,"
                       "CashOrderQuantity from `Order` where LastStatus=1 and Stock_Ticker='%s'") % (symbol)

        pending_order_arguments_rows = self.execute_responsive_sql_command(sql_command)
        pending_order_list = []
        for pending_order_arguments_row in pending_order_arguments_rows:
            received_time = TradingClass.FIXDate(pending_order_arguments_row[2])
            pending_order_arguments_row_list = list(pending_order_arguments_row)
            pending_order_arguments_row_list[2] = received_time
            pending_order_arguments_row_list[7] = int(pending_order_arguments_row_list[7])
            pending_order_arguments_row_list[8] = int(pending_order_arguments_row_list[8])
            pending_order_arguments_row_list[9] = int(pending_order_arguments_row_list[9])
            order = Order(*pending_order_arguments_row_list)
            pending_order_list.append(order)
        return pending_order_list

    def delete_all_stock_data(self):
        command = "delete from Stock"
        self.execute_nonresponsive_sql_command(command)

    def delete_stock_data(self, stock):
        command = ("delete from Stock where Ticker = '%s' limit 1" % stock.ticker)
        self.execute_nonresponsive_sql_command(command)

    def insert_stock_data(self, stock):
        command = (
            "insert into Stock(Ticker, CompanyName, LotSize, TickSize, TotalVolume) values( '%s', '%s', '%s', '%s')" % (
                stock.get_ticker, stock.get_company_name, stock.get_lot_size(), stock.get_tick_size(),
                stock.get_total_volume()))
        self.execute_nonresponsive_sql_command(command)

    def fetch_stock_information(self, stock_ticker_symbol):
        """Retrieves stock information from database

        Args:
            stock_ticker_symbol (string): The stock's ticker symbol

        Returns:
             TradingClass.DatabaseStockInformation object"""
        sql_command = (
            "SELECT CurrentPrice.CurrentPrice, PendingOrderCurrentQuantity.CurrentQuantity "
            "FROM PendingOrderCurrentQuantity INNER JOIN CurrentPrice "
            "ON PendingOrderCurrentQuantity.Ticker = CurrentPrice.Stock_Ticker")
        order_arguments_rows = self.execute_responsive_sql_command(sql_command)
        order_arguments_row_list = list(order_arguments_rows[0])
        order_arguments_row_list[0] = int(order_arguments_row_list[0])
        order_arguments_row_list[1] = int(order_arguments_row_list[1])
        database_stock_information = TradingClass.DatabaseStockInformation(*order_arguments_row_list)
        return database_stock_information

    def fetch_orders_of_type(self, order):
        """Returns all orders for the same stock as the given order


        Args:
            order (string): The user id
            password (string): The password

        Returns:
            success (ServerRespond): success of authentication
        """
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
    def __init__(self):
        self.stock_list_file_name = "stock_list.cfg"
        self.stock_list = read_file_values(self.stock_list_file_name)

    def init_market(self):
        pass
        # ServerDatabaseHandler().load_sql_file("./database/account_insert.sql")
        # ServerDatabaseHandler().load_sql_file("./database/stock_insert.sql")
        # ServerDatabaseHandler().load_sql_file("./database/order_insert.sql")
        # ServerDatabaseHandler().load_sql_file("./database/order_execution_insert.sql")

        # self.load_market_data_into_database()

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
