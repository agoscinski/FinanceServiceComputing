from tarfile import _section
import quickfix as fix
import quickfix42 as fix42
import re
import time
import datetime
import yahoo_finance
import MySQLdb
from enum import Enum
import matching_algorithm
import TradingClass
from TradingClass import MarketDataResponse
from TradingClass import NewSingleOrder
from TradingClass import OrderCancelRequest
from TradingClass import Order
from TradingClass import OrderCancelReject
from TradingClass import OrderCancelExecution
from TradingClass import OrderExecution
from TradingClass import FIXDateTimeUTC


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
        elif msg_Type.getString() == fix.MsgType_OrderCancelRequest:
            print '''IN OrderCancelRequest'''
            self.server_fix_handler.handle_order_cancel_request(message)

    def gen_exec_id(self):
        self.exec_id = self.exec_id + 1
        return self.exec_id

    def gen_order_id(self):
        self.order_id = self.order_id + 1
        return self.order_id


class ServerFIXHandler(TradingClass.FIXHandler):
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
        market_data_request = TradingClass.MarketDataRequest.from_fix_message(message)

        # Market data Object sent to server logic to be processed
        self.server_logic.process_market_data_request(market_data_request)
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
        message.setField(fix.MDReqID(market_data.md_req_id))
        message.setField(fix.NoMDEntries(market_data.no_md_entry_types))
        message.setField(fix.Symbol(market_data.symbol))
        message.setField(fix.TotalVolumeTraded(market_data.md_total_volume_traded))

        group_md_entry = fix42.MarketDataSnapshotFullRefresh.NoMDEntries()
        md_entry_type = market_data.md_entry_type_list
        md_entry_px = market_data.md_entry_px_list
        md_entry_size = market_data.md_entry_size_list
        md_entry_date = market_data.md_entry_date_list
        md_entry_time = market_data.md_entry_time_list
        entry_date_fix = fix.MDEntryDate()
        entry_time_fix = fix.MDEntryTime()
        for md_index in range(market_data.no_md_entry_types):
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

    def handle_order_request(self, fix_message):
        """Process order request from a client

            Args:
                fix_message (quickfix.Message): order fix message received from client

            Returns:
                None
        """
        fix_order = NewSingleOrder.from_fix_message(fix_message)
        self.server_logic.process_order_request(fix_order)
        return

    def handle_order_cancel_request(self, message):
        orig_cl_ord_id= TradingClass.FIXHandler.get_field_value(fix.OrigClOrdID(), message)
        cl_ord_id = TradingClass.FIXHandler.get_field_value(fix.ClOrdID(), message)
        symbol = TradingClass.FIXHandler.get_field_value(fix.Symbol(), message)
        side = TradingClass.FIXHandler.get_field_value(fix.Side(), message)
        transact_time = TradingClass.FIXHandler.get_field_string(fix.TransactTime(), message)
        order_qty = TradingClass.FIXHandler.get_field_value(fix.OrderQty(), message)
        sender_comp_id = TradingClass.FIXHandler.get_header_field_value(fix.SenderCompID(), message)
        sending_time = TradingClass.FIXHandler.get_header_field_string(fix.SendingTime(), message)
        on_behalf_of_comp_id = TradingClass.FIXHandler.get_header_field_value(fix.OnBehalfOfCompID(), message)
        sender_sub_id = TradingClass.FIXHandler.get_header_field_value(fix.SenderSubID(), message)

        # Create NewSingleOrder Object to be sent to server logic
        order_cancel_request = OrderCancelRequest (orig_cl_ord_id, cl_ord_id, symbol, side, transact_time, order_qty,
                                                   sender_comp_id, sending_time, on_behalf_of_comp_id, sender_sub_id)

        self.server_logic.process_order_cancel_request(order_cancel_request)


    def send_execution_report_respond(self, execution_report):
        """Sends an execution report respond

            Args:
                execution_report (TradingClass.ExecutionReport): the report which will be sent

            Returns:
                None
            """
        fix_message = execution_report.create_fix_message()
        fix.Session.sendToTarget(fix_message, self.fix_application.sessionID)
        return

    def send_reject_order_execution_respond(self, execution_report):
        """Send order reject execution respond

            Args:
                execution_report (TradingClass.ExecutionReport):

            Returns:
                None
            """
        fix_message = execution_report.create_fix_message()
        fix.Session.sendToTarget(fix_message, self.fix_application.sessionID)
        return


    def send_order_cancel_execution_respond(self, order_cancel_execution):
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
        header.setField(fix.MsgSeqNum(self.fix_application.exec_id))
        header.setField(fix.SendingTime())

        message.setField(fix.OrderID(order_cancel_execution.order_id))
        message.setField(fix.ClOrdID(order_cancel_execution.cl_ord_id))
        if order_cancel_execution.orig_cl_ord_id is not None:
            message.setField(fix.OrigClOrdID(order_cancel_execution.orig_cl_ord_id))
        if order_cancel_execution.price is not None:
            message.setField(fix.Price(order_cancel_execution.price))
        message.setField(fix.ExecID(order_cancel_execution.exec_id))
        message.setField(fix.ExecTransType(order_cancel_execution.exec_trans_type))
        message.setField(fix.ExecType(order_cancel_execution.exec_type))
        message.setField(fix.OrdStatus(order_cancel_execution.ord_status))
        message.setField(fix.Symbol(order_cancel_execution.symbol))
        message.setField(fix.Side(order_cancel_execution.side))
        message.setField(fix.LeavesQty(order_cancel_execution.leaves_qty))
        message.setField(fix.CumQty(order_cancel_execution.cum_qty))
        message.setField(fix.AvgPx(order_cancel_execution.avg_px))

        fix.Session.sendToTarget(message, self.fix_application.sessionID)

    def send_order_cancel_reject_respond(self, order_cancel_reject):
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelReject))

        message.setField(fix.OrderID(order_cancel_reject.order_id))
        message.setField(fix.ClOrdID(order_cancel_reject.cl_ord_id))
        message.setField(fix.OrigClOrdID(order_cancel_reject.orig_cl_ord_id))
        message.setField(fix.OrdStatus(order_cancel_reject.ord_status))
        message.setField(fix.CxlRejResponseTo(order_cancel_reject.cxl_rej_response_to))
        if order_cancel_reject.cxl_rej_reason is not None:
            message.setField(fix.CxlRejReason(order_cancel_reject.cxl_rej_reason))

        fix.Session.sendToTarget(message, self.fix_application.sessionID)
        return



class ServerLogic:
    def __init__(self, server_config_file_name, server_database_handler=None):
        self.server_fix_handler = ServerFIXHandler(self, server_config_file_name)
        self.server_database_handler = ServerDatabaseHandler() if server_database_handler == None else server_database_handler
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
        if md_request.subscription_request_type == 0:
            print("0 = Snapshot")
        elif md_request.subscription_request_type == 1:
            print("1 = Snapshot + Updates (Subscribe)")
        elif md_request.subscription_request_type == 2:
            print("2 = Disable previous Snapshot + Update Request (Un-subscribe)")

        # Now we wll only support Top of Book (only best prices quoted), Full of Book means all the traded data.
        if md_request.market_depth == 0:
            print("Full Book")
        elif md_request.market_depth == 1:
            print("Top of Book")

        md_req_id = md_request.md_req_id
        no_md_entries = md_request.no_md_entry_types
        symbol = md_request.symbol_list[0]
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
            requested_fix_order (NewSingleOrder): NewSingleOrder Object from fix handler

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
            requested_order (TradingClass.Order):
        """
        self.server_database_handler.insert_order(requested_order)
        acknowledge_execution_report = self.create_execution_report_for_new_order(requested_order)
        self.server_fix_handler.send_execution_report_respond(acknowledge_execution_report)
        orders = self.server_database_handler.fetch_pending_orders_for_stock_ticker(requested_order.symbol)
        order_executions = matching_algorithm.match(orders)
        for order_execution in order_executions:
            order_execution.execution_id = self.server_database_handler.insert_order_execution(order_execution)
            execution_report_of_buy_order, execution_report_of_sell_order = self.create_execution_report_for_order_execution(
                order_execution)
            self.server_fix_handler.send_execution_report_respond(execution_report_of_buy_order)
            self.server_fix_handler.send_execution_report_respond(execution_report_of_sell_order)
        return None

    def process_invalid_order_request(self, requested_order):
        order_id= str(self.server_fix_handler.fix_application.gen_order_id())
        exec_id=str(self.server_fix_handler.fix_application.gen_exec_id())
        cl_ord_id=requested_order.client_order_id
        receiver_comp_id=requested_order.account_company_id
        exec_trans_type='0'
        exec_type='8'
        ord_status='8'
        symbol=requested_order.stock_ticker
        side=requested_order.side
        price=requested_order.price
        stop_px=None
        leaves_qty=0
        cum_qty=0
        avg_px=0

        #Encapsulate result of processing into execution report
        reject_order_execution= OrderExecution(order_id, cl_ord_id, exec_id, exec_trans_type, exec_type, ord_status
            , symbol, side, leaves_qty, cum_qty, avg_px, price, stop_px, receiver_comp_id)
        self.server_fix_handler.send_reject_order_execution_respond(reject_order_execution)

    def check_if_order_is_valid(self, requested_order):
        stock_total_volume = self.server_database_handler.fetch_stock_total_volume(requested_order.stock_ticker)
        stock_information = self.server_database_handler.fetch_stock_information(requested_order.stock_ticker)
        current_price = stock_information.current_price

        price_difference = requested_order.price-current_price
        traded_value_difference = requested_order.price*requested_order.order_quantity-stock_total_volume*current_price

        is_valid = (0.1 >= price_difference >= -0.1 and 0.2 >= traded_value_difference >= -0.2)
        return is_valid

    def process_invalid_order_cancel_request(self, requested_order_cancel):

        order_id= str(self.server_fix_handler.fix_application.gen_order_id())
        cl_ord_id=requested_order_cancel.order_cancel_id
        orig_cl_ord_id=requested_order_cancel.client_order_id
        receiver_comp_id=requested_order_cancel.account_company_id
        ord_status='8'
        cxl_rej_response_to='1'
        cxl_rej_reason=None
        order_cancel_reject= OrderCancelReject(orig_cl_ord_id, cl_ord_id, order_id, ord_status, cxl_rej_response_to,
                                               receiver_comp_id, cxl_rej_reason)
        self.server_fix_handler.send_order_cancel_reject_respond(order_cancel_reject)


    def process_order_cancel_request(self, order_cancel_request):
        requested_order_cancel = TradingClass.OrderCancel.from_order_cancel_request(order_cancel_request)
        # TODO send Execution Report ACK MsgType 6 (Pending Cancel) only if needed
        order_cancel_is_valid = self.check_if_order_cancel_is_valid(requested_order_cancel)
        if order_cancel_is_valid:
            self.process_valid_order_cancel_request(requested_order_cancel)
        else:
            self.process_invalid_order_cancel_request(requested_order_cancel)


    def check_if_order_cancel_is_valid(self, requested_order_cancel):
        # TODO check order to be cancelled is in database
        # order = self.server_database_handler.fetch_order_by_id(requested_order_cancel.client_order_id,
        #                                                       requested_order_cancel.account_company_id)
        order = True
        if order is not None:
            return True
        else:
            return False


    def process_valid_order_cancel_request(self, requested_order_cancel):
        # TODO Insert update order cancel, order and ordercancel success
        # self.server_database_handler.insert_order_cancel(requested_order_cancel)

        # self.server_database_handler.update_order_status(requested_order_cancel.client_order_id,
        #                                        requested_order_cancel.account_company_id, OrderStatus.CANCELED)
        cumulative_quantity = 0  # TODO Query Database to retrieve quantity of order cumulatively
        executed_time = FIXDateTimeUTC.create_for_current_time()

        # self.server_database_handler.update_order_cancel_success(requested_order_cancel.client_order_id,
        #        requested_order_cancel.account_company_id, OrderCancelStatus.CANCELED, cumulative_quantity, executed_time)
        # TODO create and send Execution Report MsgType 4 ( Cancel)
        order_id = str(self.server_fix_handler.fix_application.gen_order_id())
        orig_cl_ord_id = requested_order_cancel.client_order_id
        cl_ord_id = requested_order_cancel.order_cancel_id
        exec_id = str(self.server_fix_handler.fix_application.gen_exec_id())
        receiver_comp_id = requested_order_cancel.account_company_id
        exec_trans_type = '1'
        exec_type = '4'
        ord_status = '4'
        symbol = requested_order_cancel.stock_ticker
        side = requested_order_cancel.side
        price = None
        stop_px = None
        leaves_qty = 0  # could also be filled order quantity-cum_quantity
        cum_qty = cumulative_quantity
        avg_px = 0

        # TODO provide orig_cl_ord_id mandatory in execution report for cancel
        order_cancel_execution = OrderCancelExecution(order_id, cl_ord_id, exec_id, exec_trans_type, exec_type, ord_status
                                                      , symbol, side, leaves_qty, cum_qty, avg_px, price, stop_px,
                                                      receiver_comp_id, orig_cl_ord_id)
        self.server_fix_handler.send_order_cancel_execution_respond(order_cancel_execution)

    def create_execution_report_for_new_order(self, new_order):
        """Used to create a execution report for a new order
        Args:
            new_order (TradingClass.Order):
            order_status (TradingClass.LastStatus):
        Returns:
            execution_report (TradingClass.ExecutionReport)
        """
        left_quantity = new_order.order_quantity
        cumulative_quantity = 0
        average_price = 0
        execution_report = TradingClass.ExecutionReport.from_order(new_order, TradingClass.ExecutionTransactionType.NEW,
                                                                   TradingClass.ExecutionType.NEW,
                                                                   TradingClass.OrderStatus.NEW, left_quantity,
                                                                   cumulative_quantity, average_price)
        execution_report.execution_id = self.server_database_handler.insert_execution_report(execution_report)
        return execution_report

    def create_execution_report_for_order_execution(self, order_execution):
        """Creates two execution report for the two matched orders in an order execution

        Args:
            order_execution (TradingClass.OrderExecution): The order execution matching the two orders
             for which an execution report will be created

        Returns:
            execution_report_of_buy_order (a tuple of TradingClass.ExecutionReport): The  execution report referring to
             the buy order of the two matched orders in the order execution.
            execution_report_of_sell_order (a tuple of TradingClass.ExecutionReport): The  execution report referring to
             the buy order of the two matched orders in the order execution.
        """
        execution_report_of_buy_order = self.create_execution_report_for_executed_order(
            order_execution.buyer_client_order_id, order_execution.buyer_company_id,
            order_execution.buyer_received_date, order_execution)
        execution_report_of_sell_order = self.create_execution_report_for_executed_order(
            order_execution.seller_client_order_id, order_execution.seller_company_id,
            order_execution.seller_received_date, order_execution)
        return execution_report_of_buy_order, execution_report_of_sell_order

    def create_execution_report_for_executed_order(self, client_order_id, account_company_id, received_date,
                                                   order_execution):
        """Creates an execution report for the order with the order id (client_order_id, account_company_id,
         received_date).

        Args:
            client_order_id (string): first part of order id
            account_company_id (string: second part of order id
            received_date (TradingClass.FIXDate): third part of order id
            order_execution (TradingClass.OrderExecution): The order execution to be inserted
        Returns:
            execution_report (a tuple of TradingClass.ExecutionReport): The two execution reports resulting from the
             inserted order execution. One for buy side, one for sell side.
        """
        cumulative_quantity, average_price = self.server_database_handler.fetch_cumulative_quantity_and_average_price_of_order(
            client_order_id, account_company_id, received_date)
        order = self.server_database_handler.fetch_order_for_order_id(client_order_id, account_company_id,
                                                                      received_date)
        left_quantity = order.order_quantity - cumulative_quantity
        is_order_filled = left_quantity == 0.

        if is_order_filled:
            execution_transaction_type = TradingClass.ExecutionTransactionType.FILL
            execution_type = TradingClass.ExecutionType.FILL
            order_status = TradingClass.OrderStatus.FILLED
        else:
            execution_transaction_type = TradingClass.ExecutionTransactionType.PARTIAL_FILL
            execution_type = TradingClass.ExecutionType.PARTIAL_FILL
            order_status = TradingClass.OrderStatus.PARTIALLY_FILLED

        order_id = TradingClass.Order.create_order_id(client_order_id, account_company_id, received_date)

        execution_report = TradingClass.ExecutionReport(order_id=order_id, client_order_id=client_order_id,
                                                        execution_id=order_execution.execution_id,
                                                        execution_transaction_type=execution_transaction_type,
                                                        execution_type=execution_type, order_status=order_status,
                                                        symbol=order.symbol,
                                                        side=order.side, price=order.price, left_quantity=left_quantity,
                                                        cumulative_quantity=cumulative_quantity,
                                                        average_price=average_price)
        return execution_report




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
            # TODO make this more beautiful
            order_entry_type = 0
            if pending_order.side == 1:
                order_entry_type = 0
            elif pending_order.side == 2:
                order_entry_type = 1

            if order_entry_type in market_data_entry_types:
                # TODO show how with property this can be done better
                pending_order_date_time = pending_order.received_date.date
                pending_order_fix_date = TradingClass.FIXDate.from_year_month_day(pending_order_date_time.year,
                                                                                  pending_order_date_time.month,
                                                                                  pending_order_date_time.day)
                # TODO there should be not time anymore isn it?
                # pending_order_fix_time = TradingClass.TimeFix(pending_order_date_time.hour, pending_order_date_time.minute,
                #                                           pending_order_date_time.second)

                market_data_entry_type_list.append(str(order_entry_type))
                market_data_entry_price_list.append(pending_order.price)
                market_data_entry_size_list.append(pending_order.order_quantity)
                market_data_entry_date_list.append(pending_order_fix_date)
                # market_date_entry_time_list.append(pending_order_fix_time)

        current_date_time = datetime.datetime.now()
        current_fix_date = TradingClass.FIXDate.from_year_month_day(current_date_time.year, current_date_time.month,
                                                                    current_date_time.day)
        current_fix_time = TradingClass.FIXTime(current_date_time.hour, current_date_time.minute,
                                                current_date_time.second)
        if TradingClass.MDEntryType.TRADE in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MDEntryType.TRADE)
            market_data_entry_price_list.append(stock_information.current_price)
            market_data_entry_size_list.append(0)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        # TODO Not Finished! Filled with dummy only to not cause error in client side
        # if TradingClass.MDEntryType.OPENING in market_data_entry_types_integer:
        # if 5 in market_data_entry_types_integer:
        # if 7 in market_data_entry_types_integer:
        # if 8 in market_data_entry_types_integer:

        if TradingClass.MDEntryType.OPENING in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MDEntryType.OPENING)
            market_data_entry_price_list.append(20)
            market_data_entry_size_list.append(0)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        if TradingClass.MDEntryType.CLOSING in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MDEntryType.CLOSING)
            market_data_entry_price_list.append(20)
            market_data_entry_size_list.append(0)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        if TradingClass.MDEntryType.SESSION_HIGH in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MDEntryType.SESSION_HIGH)
            market_data_entry_price_list.append(20)
            market_data_entry_size_list.append(0)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        if TradingClass.MDEntryType.SESSION_LOW in market_data_entry_types:
            market_data_entry_type_list.append(TradingClass.MDEntryType.SESSION_LOW)
            market_data_entry_price_list.append(stock_information.current_price)
            market_data_entry_size_list.append(20)
            market_data_entry_date_list.append(current_fix_date)
            market_date_entry_time_list.append(current_fix_time)

        # TODO Add Total Volume Traded but not readed from database yet!
        market_data = MarketDataResponse(market_data_required_id, len(market_data_entry_type_list), symbol,
                                         market_data_entry_type_list, market_data_entry_price_list,
                                         market_data_entry_size_list, market_data_entry_date_list,
                                         market_date_entry_time_list,
                                         stock_information.current_volume)
        return market_data


class ServerDatabaseHandler:
    def __init__(self, user_name="root", user_password="root", database_name="FSCDatabase", database_port=3306,
                 init_database_script_path="./database/init_fsc_database.sql"):
        """
        Args:
            user_name (string)
            user_password (string)
            database_name (string)
            database_port (int)
            init_database_script_path (string)
        """
        self.user_name = user_name
        self.user_password = user_password
        self.database_name = database_name
        self.database_port = database_port
        self.init_database_script_path = init_database_script_path

    def init_database(self):
        """This function initializes a new database, by first dropping the database with self.database_name and the creating
         a new one with the same name. It then load all sql files saved in the init script file located in self.init_database_script_path,
         see database documentation for file format of the init script
        """
        self.drop_schema()
        self.create_schema()
        self.load_init_script()
        return

    def teardown_database(self):
        self.drop_schema()

    def create_schema(self):
        sql_command = "CREATE SCHEMA IF NOT EXISTS `" + self.database_name + "` DEFAULT CHARACTER SET utf8 ;"
        try:
            connection = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password)
            cursor = connection.cursor()
            cursor.execute(sql_command)
            connection.commit()
            connection.close()
            return
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return

    def drop_schema(self):
        """This function drops the database with self.database_name"""
        sql_command = "DROP SCHEMA IF EXISTS `" + self.database_name + "` ;"
        self.execute_nonresponsive_sql_command(sql_command)

    def load_init_script(self):
        file_names = ServerDatabaseHandler.parse_file_names_from_init_script(self.init_database_script_path)
        for file_name in file_names:
            self.load_sql_file(file_name)
        return

    @staticmethod
    def parse_file_names_from_init_script(init_script_file_path):
        file_names = []
        pattern_for_line_with_file = re.compile("(?<=source ).+")
        for line in open(init_script_file_path):
            for match in re.finditer(pattern_for_line_with_file, line):
                file_name = match.group(0)
                file_names.append(file_name)
        return file_names

    def load_sql_file(self, file_path):
        sql_commands = ServerDatabaseHandler.parse_sql_commands_from_sql_file(file_path)
        for sql_command in sql_commands:
            self.execute_nonresponsive_sql_command(sql_command)

    @staticmethod
    def parse_sql_commands_from_sql_file(sql_file_file_path):
        """Parses a sql file and extracts the sql commands of it
        Args:
            sql_file_file_path (string): the file path of the sql file

        Returns:
            sql_commands (list of string): each element is one sql command to be executed
        """
        with open(sql_file_file_path) as sql_file:
            sql_file_content = sql_file.read().replace("\n", "").split(";")

        sql_commands = []
        pattern_for_sql_command = re.compile("(CREATE|INSERT|SET ..|UPDATE|DELETE).+")
        for block in sql_file_content:
            match = re.search(pattern_for_sql_command, block)
            if match is not None:
                sql_command = match.group(0)
                sql_commands.append(sql_command)
        return sql_commands

    def insert_execution_report(self, execution_report):
        # MAYBETODO
        return 0

    def insert_order_execution(self, order_execution):
        """Inserts an order execution and returns this order execution with an added execution ID

        Args:
            order_execution (TradingClass.OrderExecution): The order execution to be inserted

        Returns:
            order_execution_id (int): The ID of the order execution when inserted

        """
        # TODO use the insert_order function for this

        return None

    def fetch_cumulative_quantity_and_average_price_of_order(self, client_order_id, account_company_id, received_date):
        """Fetches the cumulative quantity and average price of the order with the order id (client_order_id,
         account_company_id, received_date).

        Args:
            client_order_id (string): first part of order id
            account_company_id (string: second part of order id
            received_date (TradingClass.FIXDate): third part of order id
        Returns:
            cumulative quantity (float): total number of shares filled of an order with the given order id
            average price (float): the average price of all filled shares
        """
        # TODO use execute_select_sql_command
        return 11.5, 33.33

    def fetch_order_for_order_id(self, client_order_id, account_company_id, received_date):
        """Fetches the order data of the order with the order id (client_order_id, account_company_id, received_date)
         and packs it into an order object.

        Args:
            client_order_id (string): first part of order id
            account_company_id (string: second part of order id
            received_date (TradingClass.FIXDate): third part of order id
        Returns:
            order quantity (TradingClass.Order): the order object
        """
        # TODO use execute_select_sql_command
        return TradingClass.Order.create_dummy_order()


    def fetch_latest_order_by_client_information(self, client_order_id, account_company_id):
        """Fetches the order data of the latest order with the client information (client_order_id, account_company_id)
         and packs it into an order object.

        Args:
            client_order_id (string): first part of client_information
            account_company_id (string: second part of client_information
        Returns:
            order quantity (TradingClass.Order): the order object
        """
        sql_command = ("select ClientOrderID,Account_CompanyID, ReceivedDate, HandlingInstruction, Stock_Ticker,"
                       "Side, OrderType, OrderQuantity, Price, LastStatus, MsgSeqNum, OnBehalfOfCompanyID, SenderSubID,"
                       "CashOrderQuantity from `Order` where LastStatus=1 and ClientOrderID='%s' "
                       "and Account_CompanyID='%s'") % (client_order_id, account_company_id)
        #TODO Husein return only the latest order, why do you return list?
        order_arguments_rows = self.execute_responsive_sql_command(sql_command)
        order_list = []
        for order_arguments_row in order_arguments_rows:
            received_time = TradingClass.FIXDate(order_arguments_row[2])
            order_arguments_row_list = list(order_arguments_row)
            order_arguments_row_list[2] = received_time
            order_arguments_row_list[7] = int(order_arguments_row_list[7])
            order_arguments_row_list[8] = int(order_arguments_row_list[8])
            order_arguments_row_list[9] = int(order_arguments_row_list[9])
            order = TradingClass.Order(*order_arguments_row_list)
            order_list.append(order)
        return order_list


    def insert_order(self, order):
        """Inserts a TradingClass.Order into the database

        Args:
            order (TradingClass.Order): The order to be inserted

        Returns:
            order_id (string): the order id from the order inserted, if it is None, then insertion failed
        """
        command = (
            "INSERT INTO `Order`(ClientOrderID, Account_CompanyID, ReceivedDate, HandlingInstruction, Stock_Ticker,"
            "Side, MaturityDate, OrderType, OrderQuantity, Price, LastStatus, MsgSeqNum) VALUES('%s','%s','%s','%s','%s','%s',"
            "'%s','%s','%s','%s','%s', '%s')"
            % (order.client_order_id, order.account_company_id, str(order.received_date),
               order.handling_instruction, order.stock_ticker, str(order.side),
               str(order.maturity_date), order.order_type, str(order.order_quantity),
               str(order.price), str(order.last_status), str(order.msg_seq_num)))
        order_id = self.execute_nonresponsive_sql_command(command)
        return order_id

    def execute_select_sql_command(self, sql_command):
        """Used to execute SELECT commands which return a table
        Args:
            sql_command (string): the sql command to be executed
        Returns:
            fetched_database_rows (list of tuples): the each entry is a row of the select statement #TODO do not know if this is correct
        """
        fetched_database_rows = []
        try:
            connection = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                         db=self.database_name, port=self.database_port)
            cursor = connection.cursor()
            execution = (sql_command)
            cursor.execute(execution)
            fetched_database_rows = cursor.fetchall()
            connection.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        return fetched_database_rows

    def execute_nonresponsive_sql_command(self, sql_command):
        """Used to execute commands CREATE, UPDATE, DELETE which returns nothing
        Args:
            sql_command (string): the sql command to be executed
        Returns:
            None
        """
        try:
            connection = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                         db=self.database_name, port=self.database_port)
            cursor = connection.cursor()
            cursor.execute(sql_command)
            connection.commit()
            connection.close()
            return
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def execute_responsive_insert_sql_command(self, insert_sql_command):
        """Used to execute commands INSERT which returns the produced ID from database server
        Args:
            insert_sql_command (string): the sql command to be executed
        Returns:
            id_of_inserted_row (ID type in database): the ID of the object inserted
        """
        try:
            connection = MySQLdb.connect(host='localhost', user=self.user_name, passwd=self.user_password,
                                         db=self.database_name, port=self.database_port)
            cursor = connection.cursor()
            cursor.execute(insert_sql_command)
            connection.commit()
            id_of_inserted_row = connection.lastrowid()
            connection.close()
            return id_of_inserted_row
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def insert_order_cancel(self, requested_order_cancel):
        #TODO Husein figure out who does it
        sql_command =""
        self.execute_nonresponsive_sql_command(sql_command)

    def update_order_status(self, client_order_id, account_company_id, order_status):
        #TODO Husein figure out who does it
        sql_command = ""
        self.execute_nonresponsive_sql_command(sql_command)

    def update_order_cancel_success(self, client_order_id, account_company_id, order_cancel_status, cumulative_quantity,
                                    executed_time):
        #TODO Husein figure out who does it
        sql_command =""
        self.execute_nonresponsive_sql_command(sql_command)

    def fetch_pending_orders_for_stock_ticker(self, symbol):
        """Fetches all orders from the database with status not finished

        Args:
            symbol (string): The ticker symbol for which orders are fetched
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

    def fetch_pending_orders_for_stock_ticker(self, symbol):
        """Fetches all orders from the database with status not finisheddern

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
                stock.ticker, stock.company_name, stock.lot_size, stock.tick_size, stock.total_volume))
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

    def fetch_stock_total_volume(self, stock_ticker_symbol):
        """Retrieves stock total volume from database

        Args:
            stock_ticker_symbol (string): The stock's ticker symbol

        Returns:
             Stock Total Volume (float)"""
        sql_command = ("SELECT TotalVolume FROM Stock where Ticker='%s'" % stock_ticker_symbol)
        stock_arguments_rows = self.execute_responsive_sql_command(sql_command)
        stock_total_volume = stock_arguments_rows[0][0]

        return stock_total_volume

    def fetch_orders_of_type(self, order):
        """Returns all orders for the same stock as the given order


        Args:
            order (string): The user id
            password (string): The password

        Returns:
            success (ServerRespond): success of authentication
        """
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
