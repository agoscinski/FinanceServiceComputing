import re
import datetime
import quickfix as fix
import quickfix42 as fix42

##################
## Time classes ##
##################

class FIXYearMonth(object):
    def __init__(self, date_object):
        self.date = date_object

    @classmethod
    def from_year_month(cls, year, month):
        """Constructor of YearMonthFix
        Args:
            year (int)
            month (int)
        """
        date_object = datetime.date(year, month, 1)
        return cls(date_object)

    @classmethod
    def from_date_stamp_string(cls, date_stamp_string):
        """Constructor from date stamp strings

        Args:
            date_stamp_string (string): string in format YYYYMM
        Returns:
            (FIXYearMonth object)
        """
        date_object = datetime.datetime.strptime(date_stamp_string, "%Y%m").date()
        return cls(date_object)

    @property
    def year(self):
        return self.date.year

    @year.setter
    def year(self, year):
        self.date.year = year

    @property
    def month(self):
        return self.date.month

    @month.setter
    def month(self, month):
        self.date.month = month

    def __str__(self):
        return self.month_year.strftime("%Y%m")

    # TODO remove
    def get_year_month(self):
        return self.month_year

    def set_year_month(self, year, month):
        self.month_year = datetime.date(year, month, 1)

    def set_year_month_string(self, string):
        self.month_year = datetime.datetime.strptime(string, "%Y%m").date()

    def set_year_month_value(self, date):
        self.month_year = date


class FIXDate(object):
    """The FixDate object encapsulates a date object

    Attributes:
        date (datetime.date): the date
    """

    def __init__(self, date_object):
        self.date = date_object

    @classmethod
    def from_fix_date_stamp_string(cls, date_stamp_string):
        """Constructor for mysql date stamp strings

        Args:
            date_stamp_string (string): string in format YYYYMMDD
        Returns:
            (FIXDate object)
        """
        date_object = datetime.datetime.strptime(date_stamp_string, "%Y%m%d").date()
        return cls(date_object)

    @classmethod
    def from_mysql_date_stamp_string(cls, date_stamp_string):
        """Constructor for mysql date stamp strings

        Args:
            date_stamp_string (string): string in format YYYY-MM-DD
        Returns:
            (FIXDate object)
        """
        date_object = datetime.datetime.strptime(date_stamp_string, "%Y-%m-%d").date()
        return cls(date_object)

    @classmethod
    def from_year_month_day(cls, year, month, day):
        """Constructor from date stamp strings

        Args:
            year (int): an integer representing the year
            month (int): an integer representing the month
            day (int): an integer representing the day
        Returns:
            (FIXDate object)
        """
        date_object = datetime.date(year, month, day)
        return cls(date_object)

    def __eq__(self, other):
        return self.date.year == other.date.year and self.date.month == other.date.month and self.date.day == other.date.day

    def __ne__(self, other):
        return not __eq__(self, other)

    def __str__(self):
        return self.date.strftime("%Y%m%d")

    @property
    def mysql_date_stamp_string(self):
        return self.date.strftime("%Y-%m-%d")

    @mysql_date_stamp_string.setter
    def year(self, date_stamp_string):
        self.date = datetime.datetime.strptime(date_stamp_string, "%Y-%m-%d").date()

    @property
    def year(self):
        return self.date.year

    @year.setter
    def year(self, year):
        self.date.year = year

    @property
    def month(self):
        return self.date.month

    @month.setter
    def month(self, month):
        self.date.month = month

    @property
    def day(self):
        return self.date.day

    @day.setter
    def day(self, day):
        self.date.day = day

    # TODO remove
    def set_date_from_year_month_day(self, year, month, date):
        self.date = datetime.date(year, month, date)

    def set_date_from_date_stamp_string(self, string):
        self.date = datetime.datetime.strptime(string, "%Y-%m-%d").date()

    def set_date_today(self):
        self.date = datetime.date.today()


class FIXTime(object):
    """Constructor of FIXTime
        @Parameter:
            hour : hour in int
            minute : minutes in int
            second : second in int
    """

    def __init__(self, hour, minute, second):
        self.time = datetime.time(hour, minute, second, 0)

    # TODO remove
    def get_time(self):
        return self.time

    def __str__(self):
        return self.time.strftime("%H:%M:%S")

    # TODO remove
    def set_time(self, hour, minute, second):
        self.time = datetime.time(hour, minute, second, 0)

    def set_time_string(self, string):
        self.time = datetime.datetime.strptime(string, "%H:%M:%S").time()

    def set_time_value(self, time):
        self.time = time


class FIXDateTimeUTC(object):
    def __init__(self, datetime_object):
        """Constructor of FIXDateTimeUTC from
        Args:
            datetime_object (datetime.datetime object)
        """
        self.date_time = datetime_object

    @classmethod
    def from_year_month_date_hour_minute_second(cls, year, month, date, hour, minute, second):
        """Constructor of FIXDateTimeUTC
        Args
            year (int): year
            month (int): month
            date (int): date
            hour (int): hour
            minute (int): minutes
            second (int): second
        """
        datetime_object = datetime.datetime(year, month, date, hour, minute, second, 0)
        return cls(datetime_object)

    @classmethod
    def create_for_current_time(cls):
        current_time_datetime_object = datetime.datetime.utcnow()
        return cls(current_time_datetime_object)

    @classmethod
    def from_date_fix_time_stamp_string(cls, date_time_stamp_string):
        """Constructor from date stamp strings
    @staticmethod
    def parse_file_names_from_init_script(init_script_file_path):
        file_names = []
        pattern_for_line_with_file = re.compile("(?<=source ).+")
        for line in open(init_script_file_path):
            for match in re.finditer(pattern_for_line_with_file, line):
                file_name = match.group(0)
                file_names.append(file_name)
        return file_names

        Args:
            date_time_stamp_string (string): string in format YYYYMMDD-HH:MM:SS
        Returns:
            (FIXDate object)
        """
        date_object = datetime.datetime.strptime(date_time_stamp_string, "%Y%m%d-%H:%M:%S").date()
        return cls(date_object)

    def __str__(self):
        return self.date_time.strftime("%Y%m%d-%H:%M:%S")

    @property
    def mysql_date_stamp_string(self):
        return self.date.strftime("%Y-%m-%d %H:%M:%S")

    @mysql_date_stamp_string.setter
    def year(self, date_stamp_string):
        self.date = datetime.datetime.strptime(date_stamp_string, "%Y-%m-%d %H:%M:%S").date()

    # TODO clean
    def get_date_time(self):
        return self.date_time

    def set_date_time(self, year, month, date, hour, minute, second):
        self.date_time = datetime.datetime(year, month, date, hour, minute, second, 0)

    def set_date_time_string(self, string):
        self.date_time = datetime.datetime.strptime(string, "%Y%m%d-%H:%M:%S").date()

    def set_date_time_default_string(self, string):
        self.date_time = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").date()

    def set_date_time_value(self, date_time):
        self.date_time = date_time


###################################
## Server/Client related classes ##
###################################

class FIXHandlerUtils:

    class MarketDataEntryType:
        OFFER = 0
        BID = 1
        CURRENT_PRICE = 2
        OPENING_PRICE = 4
        CLOSING_PRICE = 5
        DAY_HIGH = 7
        DAY_LOW = 8

    class Side:
        BUY = fix.Side_BUY
        SELL = fix.Side_SELL

    class OrderType:
        MARKET = fix.TriggerOrderType_MARKET
        LIMIT = fix.TriggerOrderType_LIMIT

    class OrderStatus:
        NEW = 2
        REPLACED = 3
        PARTIALLY_FILLED = 4
        EXPIRED = 5
        CANCELED = 6
        FILLED = 8
        PENDING_REPLACE = 11
        PENDING_CANCEL = 12

    class ExecutionType:
        NEW = 0
        PARTIAL_FILL = 1
        FILL = 2
        CANCELED = 4
        REJECTED = 8

    class ExecutionTransactionType:
        NEW = '0'
        PARTIAL_FILL = '1'
        FILL = '2'
        CANCELED = '4'
        REPLACE = '5'
        REJECTED = '8'
        EXPIRED = 'C'

    class HandlingInstruction:
        AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION = fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION

    @staticmethod
    def get_field_value(fix_object, message):
        if message.isSetField(fix_object.getField()):
            message.getField(fix_object)
            return fix_object.getValue()
        else:
            return None

    @staticmethod
    def get_field_string(fix_object, message):
        if message.isSetField(fix_object.getField()):
            message.getField(fix_object)
            return fix_object.getString()
        else:
            return None

    @staticmethod
    def get_header_field_value(fix_object, message):
        if message.getHeader().isSetField(fix_object.getField()):
            message.getHeader().getField(fix_object)
            return fix_object.getValue()
        else:
            return None

    @staticmethod
    def get_header_field_string(fix_object, message):
        if message.getHeader().isSetField(fix_object.getField()):
            message.getHeader().getField(fix_object)
            return fix_object.getString()
        else:
            return None

class DatabaseHandlerUtils:
    # Enums
    class OrderType:
        MARKET = 1
        LIMIT = 2

    class Side:
        BUY = 1
        SELL = 2

    class LastStatus:
        DONE = 0
        PENDING = 1
        CANCELED = 2
        EXPIRED = 3

    class HandlingInstruction:
        AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION = 1

    @staticmethod
    def parse_file_names_from_init_script(init_script_file_path):
        file_names = []
        pattern_for_line_with_file = re.compile("(?<=source ).+")
        for line in open(init_script_file_path):
            for match in re.finditer(pattern_for_line_with_file, line):
                file_name = match.group(0)
                file_names.append(file_name)
        return file_names

    @staticmethod
    def parse_sql_commands_from_sql_file(sql_file_file_path):
        """Parses a sql file and extracts the sql commands of it
        Args:
            sql_file_file_path (string): the file path of the sql file

        Returns:
            sql_commands (list of string): each element is one sql command to be executed
        """
        with open(sql_file_file_path) as sql_file:
            sql_file_content = sql_file.read().replace("\n", " ").split(";")

        sql_commands = []
        pattern_for_sql_command = re.compile("(CREATE|INSERT|SET ..|UPDATE|DELETE).+")
        for block in sql_file_content:
            match = re.search(pattern_for_sql_command, block)
            if match is not None:
                sql_command = match.group(0)
                sql_commands.append(sql_command)
        return sql_commands


#################################
## FIX message related classes ##
#################################

class MarketDataRequest(object):
    """Constructor of class MarketDataRequest:
    Args:
        md_req_id (string): market data request ID
        subscription_request_type : Type of subscription of market data request (char)
        market_depth : market depth of market data request (int)
        no_md_entry_types (int) : number of market data entry requested
        md_entry_type_list (list of int): market data entries
        no_related_sym : number of symbols requested (int)
        symbol_list : list of ticker symbol (list of string)
    """

    def __init__(self, md_req_id, subscription_request_type, market_depth, no_md_entry_types, md_entry_type_list,
                 no_related_sym, symbol_list):
        self.md_req_id = md_req_id
        self.subscription_request_type = subscription_request_type
        self.market_depth = market_depth
        self.no_md_entry_types = no_md_entry_types
        self.md_entry_type_list = md_entry_type_list
        self.no_related_sym = no_related_sym
        self.symbol_list = symbol_list

    @classmethod
    def from_fix_message(cls, fix_message):
        """Constructor from a quickfix.Message"""
        message_fields = [fix.MDReqID(), fix.SubscriptionRequestType(), fix.MarketDepth(), fix.NoMDEntryTypes(),
                          fix.NoRelatedSym()]
        market_data_required_id, subscription_request_type, market_depth, no_market_data_entry_types, no_related_symbols = get_values_from_fix_message_fields(
            fix_message, message_fields)

        market_data_entry_types = get_fix_group_field(fix_message, fix42.MarketDataRequest().NoMDEntryTypes(),
                                                      fix.MDEntryType(), no_market_data_entry_types,
                                                      transform_group_element=int)
        related_symbols = get_fix_group_field(fix_message, fix42.MarketDataRequest().NoRelatedSym(), fix.Symbol(),
                                              no_related_symbols)

        market_data_request = cls(market_data_required_id, subscription_request_type, market_depth,
                                  no_market_data_entry_types, market_data_entry_types, no_related_symbols,
                                  related_symbols)
        return market_data_request


# TODO Move this functions to FIXHandler
def get_values_from_fix_message_fields(fix_message, message_field_types):
    """Gets the values of the message fields in the message
    Args:
        fix_message (quickfix.Message)
        message_field_types (list of quickfix field types)
    Returns:
        values (list of different types)"""
    values = []
    for i in range(len(message_field_types)):
        fix_field = message_field_types[i]
        fix_message.getField(fix_field)
        values[i] = fix_field.getValue()
    return values


def get_fix_group_field(fix_message, fix_group, fix_field_type, no_group_elements,
                        transform_group_element=None):
    """
    Args:
        fix_message (quickfix.Message):
        fix_group (FIX::Group *)
        fix_field_type (quickfix field type)
        no_group_elements (int)
        transform_group_element (function): This function is applied on each group entry after the value is
            retrieved
    Returns:
        group_elements (list of different types): list of group elements
    """
    group_elements = []
    for i in range(no_group_elements):
        fix_message.getGroup(i + 1, fix_group)
        fix_group.getField(fix_field_type)
        group_element = fix_field_type.getValue() if transform_group_element is None else transform_group_element(
            fix_field_type.getValue())
        group_elements.append(group_element)
    return group_elements


class MarketDataResponse(object):
    """Constructor of class MarketDataResponse:
        @Parameter:
            md_req_id : market data response ID related to market data request ID (string)
            no_md_entry_types = no_md_entry_types (int)
            symbol = symbol (string)
            md_entry_type_list = md entry type list (list of int)
            md_entry_px_list = md entry price list (list of float)
            md_entry_size_list = md entry size list (list of float)
            md_entry_date_list = md entry date list (list of DateFix Object=> datetime UTC Date YYYYMMDD)
            md_entry_time_list = md entry time list (list of TimeFix Object=> datetime UTC Time HH:MM:SS)
    """

    def __init__(self, md_req_id, no_md_entry_types, symbol, md_entry_type_list, md_entry_px_list,
                 md_entry_size_list, md_entry_date_list, md_entry_time_list, md_total_volume_traded=None):
        self.md_req_id = md_req_id
        self.no_md_entry_types = no_md_entry_types
        self.symbol = symbol
        self.md_entry_type_list = md_entry_type_list
        self.md_entry_px_list = md_entry_px_list
        self.md_entry_size_list = md_entry_size_list
        self.md_entry_date_list = md_entry_date_list
        self.md_entry_time_list = md_entry_time_list
        self.md_total_volume_traded = md_total_volume_traded


class OrderCancelRequest(object):
    """Constructor of class OrderCancelRequest:
        @Parameter:
        orig_cl_ord_id = original client order id to be cancelled (String)
        cl_ord_id = cancellation client order id (String)
        symbol = symbol (String)
        side = side (char)
        transact_time = transaction time (DateTimeFix Object=> DateTime datetime UTC YYYYMMDD-HH:MM:SS)
        order_qty = order quantity (float)
        sender_comp_id = sender company id (String)
        sending_time = Sending Time of the message (DateTimeFix Object=> DateTime datetime UTC YYYYMMDD-HH:MM:SS)
        on_behalf_of_comp_id = company on behalf of sender company id (String)
        sender_sub_id = identifier created by sender_comp_id (String)
    """

    def __init__(self, orig_cl_ord_id, cl_ord_id, symbol, side, transact_time, order_qty, sender_comp_id=None,
                 sending_time=None, on_behalf_of_comp_id=None, sender_sub_id=None):
        self.orig_cl_ord_id = orig_cl_ord_id
        self.cl_ord_id = cl_ord_id
        self.symbol = symbol
        self.side = side
        self.transact_time = transact_time
        self.order_qty = order_qty
        self.sender_comp_id = sender_comp_id
        if sending_time is not None:
            self.sending_time = sending_time
        if sender_comp_id is not None:
            self.sender_comp_id = sender_comp_id
        if on_behalf_of_comp_id is not None:
            self.on_behalf_of_comp_id = on_behalf_of_comp_id
        if sender_sub_id is not None:
            self.sender_sub_id = sender_sub_id


class OrderCancelReject(object):
    """Constructor of class OrderCancelReject represents a quickfix order cancel reject (message type 9):
    Args:
        orig_cl_ord_id=original client order id to be cancelled (String)
        cl_ord_id= cancellation client order id (String)
        order_id= Execution Order Cancel ID  (String)
        ord_status= status of rejected order cancel =8 (Char)
        cxl_rej_response_to= type of transaction requested=> OrderCancelRequest =1 (Char)
        receiver_comp_id= receiver company ID (String)

    """

    def __init__(self, orig_cl_ord_id, cl_ord_id, order_id, ord_status, cxl_rej_response_to, receiver_comp_id=None,
                 cxl_rej_reason=None):
        self.orig_cl_ord_id = orig_cl_ord_id
        self.cl_ord_id = cl_ord_id
        self.order_id = order_id
        self.ord_status = ord_status
        self.cxl_rej_response_to = cxl_rej_response_to
        # TODO Husein ? why this ifs
        if receiver_comp_id is not None:
            self.sender_comp_id = receiver_comp_id
        else:
            self.sender_comp_id = None
        if cxl_rej_reason is not None:
            self.cxl_rej_reason = cxl_rej_reason
        else:
            self.cxl_rej_reason = None


class NewSingleOrder(object):
    """A New single order is designed after the FIX message of type D "Order - Single" and is used to
     encapsulate a message into an object

    Args:
        client_order_id (string)
        handling_instruction (char/FIXHandler.HandlingInstruction)
        symbol (string)
        side (char/FIXHandler.Side)
        maturity_month_year (FIXYearMonth)
        maturity_day (int): between 1-31
        transaction_time (FIXDateTime)
        order_quantity (float)
        order_type (char/FIXHandler.OrderType)
        price (float)
        stop_price (float)
    """

    def __init__(self, client_order_id, handling_instruction, symbol, maturity_month_year,
                 maturity_day, side, transaction_time, order_quantity, order_type, price, stop_price,
                 sender_company_id, sending_time, on_behalf_of_comp_id, sender_sub_id):
        self.client_order_id = client_order_id
        self.handling_instruction = handling_instruction
        self.symbol = symbol
        self.maturity_month_year = maturity_month_year
        self.maturity_day = maturity_day
        self.side = side
        self.transaction_time = transaction_time
        self.order_quantity = order_quantity
        self.order_type = order_type
        self.price = price
        self.stop_price = stop_price
        self.sender_company_id = sender_company_id
        self.sending_time = sending_time
        self.on_behalf_of_comp_id = on_behalf_of_comp_id
        self.sender_sub_id = sender_sub_id

    @classmethod
    def create_dummy_new_single_order(cls, client_order_id="client", handling_instruction="1",
                                      symbol="TSLA", maturity_month_year=FIXYearMonth.from_year_month(2000, 1),
                                      maturity_day=2, side=FIXHandlerUtils.Side.BUY,
                                      transaction_time=FIXDateTimeUTC.from_date_fix_time_stamp_string("20000101-10:00:00"),
                                      order_quantity=10., order_type=FIXHandlerUtils.OrderType.LIMIT, price=100.,
                                      stop_price=None, sender_company_id=None, sending_time=None,
                                      on_behalf_of_company_id=None, sender_sub_id=None):
        """For testing"""
        dummy_new_single_order = cls(client_order_id, handling_instruction,
                                     symbol, maturity_month_year, maturity_day, side,
                                     transaction_time, order_quantity, order_type, price,
                                     stop_price, sender_company_id, sending_time,
                                     on_behalf_of_company_id, sender_sub_id)
        return dummy_new_single_order

    @classmethod
    def from_fix_message(cls, fix_message):
        """Constructor from a quickfix.Message
        Args:
           fix_message (quickfix.Message)
        Returns:
            NewSingleOrder
        """
        client_order_id = FIXHandlerUtils.get_field_value(fix.ClOrdID(), fix_message)
        handling_instruction = FIXHandlerUtils.get_field_value(fix.HandlInst(), fix_message)
        execution_instruction = FIXHandlerUtils.get_field_value(fix.ExecInst(), fix_message)
        symbol = FIXHandlerUtils.get_field_value(fix.Symbol(), fix_message)
        maturity_month_year = FIXHandlerUtils.get_field_value(fix.MaturityMonthYear(), fix_message)
        maturity_day = FIXHandlerUtils.get_field_value(fix.MaturityDay(), fix_message)
        side = FIXHandlerUtils.get_field_value(fix.Side(), fix_message)
        transact_time = FIXHandlerUtils.get_field_string(fix.TransactTime(), fix_message)
        order_quantity = FIXHandlerUtils.get_field_value(fix.OrderQty(), fix_message)
        order_type = FIXHandlerUtils.get_field_value(fix.OrdType(), fix_message)
        price = FIXHandlerUtils.get_field_value(fix.Price(), fix_message)
        stop_price = FIXHandlerUtils.get_field_value(fix.StopPx(), fix_message)
        sender_company_id = FIXHandlerUtils.get_header_field_value(fix.SenderCompID(), fix_message)
        sending_time = FIXHandlerUtils.get_header_field_string(fix.SendingTime(), fix_message)
        on_behalf_of_comp_id = FIXHandlerUtils.get_header_field_value(fix.OnBehalfOfCompID(), fix_message)
        sender_sub_id = FIXHandlerUtils.get_header_field_value(fix.SenderSubID(), fix_message)
        return cls(client_order_id, handling_instruction, execution_instruction, symbol, maturity_month_year,
                   maturity_day, side,
                   transact_time, order_quantity, order_type, price, stop_price, sender_company_id,
                   sending_time, on_behalf_of_comp_id, sender_sub_id)


class ExecutionReport(object):
    """Constructor
    Args:
        order_id (string): order id
        client_order_id (string): client order id
        execution_id (string): execution id
        execution_transaction_type (char): execution transaction type
        execution_type (char): execution type
        order_status (char):
        symbol (String): ticker symbol of the stock
        side (char):
        left_quantity (float): amount of shares open for further execution
        cumulative_quantity (float): total number of shares filled
        average_price (float): calculated average price of all fills on this order
        price (float):
    """

    def __init__(self, order_id, client_order_id, execution_id, execution_transaction_type, execution_type,
                 order_status, symbol, side, left_quantity
                 , cumulative_quantity, average_price, price, receiver_comp_id=None):
        self.order_id = order_id
        self.client_order_id = client_order_id
        self.execution_id = execution_id
        self.execution_transaction_type = execution_transaction_type
        self.execution_type = execution_type
        self.order_status = order_status
        self.symbol = symbol
        self.side = side
        self.left_quantity = left_quantity
        self.cumulative_quantity = cumulative_quantity
        self.average_price = average_price
        self.price = price
        self.receiver_comp_id = receiver_comp_id

    @classmethod
    def from_order(cls, order, execution_transaction_type, execution_type, order_status, left_quantity,
                   cumulative_quantity, average_price):
        """
        Args:
            order (TradingClass.Order)
            execution_transaction_type (char)
            execution_type (int)
            order_status (int)
            left_quantity (float): amount of shares open for further execution
            cumulative_quantity (float): total number of shares filled
            average_price (float): calculated average price of all fills on this order
        """
        order_id = order.order_id
        client_order_id = order.client_order_id
        execution_id = None
        # execution_transaction_type
        # str(execution_type)
        # str(order_status)
        symbol = order.stock_ticker
        side = order.side
        # left_quantity
        # cumulative_quantity
        # average_price
        price = order.price
        execution_report = cls(order_id, client_order_id, execution_id, execution_transaction_type, str(execution_type),
                               str(order_status), symbol, side, left_quantity, cumulative_quantity, average_price,
                               price)
        return execution_report

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def create_fix_message(self):
        """Creates from an execution report a fix message"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
        header.setField(fix.SendingTime())

        message.setField(fix.OrderID(self.order_id))
        message.setField(fix.ClOrdID(self.client_order_id))
        message.setField(fix.ExecID(self.execution_id))
        message.setField(fix.ExecTransType(self.execution_transaction_type))
        message.setField(fix.ExecType(self.execution_type))
        message.setField(fix.OrdStatus(self.order_status))
        message.setField(fix.Symbol(self.symbol))
        message.setField(fix.Side(self.side))
        message.setField(fix.LeavesQty(self.left_quantity))
        message.setField(fix.CumQty(self.cumulative_quantity))
        message.setField(fix.AvgPx(self.average_price))
        message.setField(fix.Price(self.price))
        return message


class Order(object):
    """Constructor of class Order, it is designed after the Order table from the database
    Args:
        client_order_id (string): The order ID from the client side
        account_company_id (string): account company id related to the order
        received_date (FIXDate object): received_date
        handling_instruction (int/DatabaseHandler.HandlingInstruction): handling instruction
        stock_ticker (string): ticker symbol of the stock referring in the order
        side (int/DatabaseHandler.Side): type of order
        maturity_date (FIXDate object): the date when order will mature
        order_type (int/DatabaseHandler.OrderType): the type of order, see Side for different types
        order_quantity (float): order quantity
        price (float): price of the stock
        last_status (int/DatabaseHandler.LastStatus): last status
        msg_seq_num (int): message sequence number
        on_behalf_of_company_id (string): original sender who sends order
        sender_sub_id (string): sub identifier of sender
        cash_order_quantity (float): amount of order requested
        msg_seq_num (int)
    """

    def __init__(self, client_order_id, account_company_id, received_date, handling_instruction, stock_ticker, side,
                 maturity_date,
                 order_type, order_quantity, price, last_status, msg_seq_num=None, on_behalf_of_company_id=None,
                 sender_sub_id=None, cash_order_quantity=None):
        self.client_order_id = client_order_id
        self.account_company_id = account_company_id
        self.received_date = received_date
        self.handling_instruction = handling_instruction
        self.stock_ticker = stock_ticker
        self.side = side
        self.maturity_date = maturity_date
        self.order_type = order_type
        self.order_quantity = order_quantity
        self.price = price
        self.last_status = last_status
        self.msg_seq_num = msg_seq_num
        self.on_behalf_of_company_id = on_behalf_of_company_id
        self.sender_sub_id = sender_sub_id
        self.cash_order_quantity = cash_order_quantity

    @classmethod
    def create_dummy_order(cls, client_order_id="20161120-001", account_company_id="client",
                           received_date=FIXDate.from_fix_date_stamp_string("20161120"), handling_instruction=1,
                           stock_ticker="TSLA", side=DatabaseHandlerUtils.Side.BUY, maturity_date=FIXDate.from_fix_date_stamp_string("20161125"),
                           order_type=DatabaseHandlerUtils.OrderType.MARKET, order_quantity=100.00, price=10.00,
                           last_status=DatabaseHandlerUtils.LastStatus.PENDING, msg_seq_num=0):
        """For testing"""
        dummy_order = cls(client_order_id=client_order_id, account_company_id=account_company_id,
                          received_date=received_date, handling_instruction=handling_instruction,
                          stock_ticker=stock_ticker, side=side, maturity_date=maturity_date, order_type=order_type,
                          order_quantity=order_quantity, price=price, last_status=last_status, msg_seq_num=msg_seq_num)
        return dummy_order

    @classmethod
    def from_new_single_order(cls, new_single_order):
        """Creates a order from a TradingClass.NewSingleOrder
        Args:
            new_single_order (TradingClass.NewSingleOrder):
        Returns:
            order (TradingClass.Order): The order object
        """

        client_order_id = new_single_order.client_order_id
        account_company_id = new_single_order.sender_company_id
        received_time = FIXDateTimeUTC.create_for_current_time()
        handling_instruction = new_single_order.handling_instruction
        stock_ticker = new_single_order.symbol
        side = new_single_order.side
        maturity_date = FIXDate.from_year_month_day(new_single_order.maturity_month_year.year,
                                                    new_single_order.maturity_month_year.month,
                                                    new_single_order.maturity_day)
        order_type = new_single_order.order_type
        order_quantity = new_single_order.order_quantity
        price = new_single_order.price
        last_status = DatabaseHandlerUtils.LastStatus.PENDING
        message_sequence_number = 0
        on_behalf_of_company_id = None
        sender_sub_id = None
        cash_order_quantity = None

        order = cls(client_order_id, account_company_id, received_time, handling_instruction, stock_ticker,
                    side, maturity_date, order_type, order_quantity, price, last_status, message_sequence_number,
                    on_behalf_of_company_id, sender_sub_id, cash_order_quantity)
        return order

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    @property
    def order_id(self):
        """
        Returns:
             order_id (string):
        """
        return Order.create_order_id(self.client_order_id, self.account_company_id, self.received_date)

    @staticmethod
    def create_order_id(client_order_id, account_company_id, received_date):
        """Creates an order id from the components. Use this method if you want
         to create an order id

        Args:
            client_order_id (string)
            account_company_id (string)
            received_date (TradingClass.FIXDate)
        Returns:
             order_id (string):
        """
        return client_order_id + "_" + account_company_id + "_" + str(received_date)


# TODO Husein merge ExecutionReport
class OrderCancelExecution(object):
    """Constructor
        @Parameter:
            order_id = order id (String)
            cl_ord_id = client order id (String)
            exec_id = execution id (String)
            exec_trans_type = execution transaction type (char)
            exec_type = execution type (char)
            ord_status = order status (char)
            symbol = symbol (String)
            side = side (char)
            leaves_qty = quantity leaves to be fulfiled (float)
            cum_qty = cumulative quantity (float)
            avg_px = average price (float)
            price = price (float)
            stop_px = stop price (float)
        """

    def __init__(self, order_id, cl_ord_id, exec_id, exec_trans_type, exec_type, ord_status, symbol, side,
                 leaves_qty, cum_qty, avg_px, price, stop_px, receiver_comp_id=None, orig_cl_ord_id=None):
        self.order_id = order_id
        self.cl_ord_id = cl_ord_id
        self.exec_id = exec_id
        self.exec_trans_type = exec_trans_type
        self.exec_type = exec_type
        self.ord_status = ord_status
        self.symbol = symbol
        self.side = side
        self.leaves_qty = leaves_qty
        self.cum_qty = cum_qty
        self.avg_px = avg_px
        self.price = price
        self.stop_px = stop_px
        self.receiver_comp_id = receiver_comp_id
        if orig_cl_ord_id is not None:
            self.orig_cl_ord_id = orig_cl_ord_id
        else:
            self.orig_cl_ord_id = None


################################
### Database related classes ###
################################


class DatabaseStockInformation:
    def __init__(self, current_price=None, current_volume=None, opening_price=None, closing_price=None,
                 day_high=None,
                 day_low=None):
        self.current_price = current_price
        self.current_volume = current_volume
        self.opening_price = opening_price
        self.closing_price = closing_price
        self.day_high = day_high
        self.day_low = day_low


class OrderExecution:
    def __init__(self, execution_id, quantity, price, execution_time, buyer_client_order_id,
                 buyer_company_id, buyer_received_date, seller_client_order_id, seller_company_id,
                 seller_received_date):
        """
        Args:
            execution_id (int)
            quantity (float): quantity of the order execution
            price (float): price of the order execution (the price on which both parties execute order)
            execution_time (TradingClass.FIXDateTimeUTC): date and time of execution
            buyer_client_order_id (string)
            buyer_company_id (string)
            buyer_received_date (TradingClass.FIXDate)
            seller_client_order_id (string)
            seller_company_id (string)
            seller_received_date (string)
        """
        self.execution_id = execution_id
        self.quantity = quantity
        self.price = price
        self.execution_time = execution_time
        self.buyer_client_order_id = buyer_client_order_id
        self.buyer_company_id = buyer_company_id
        self.buyer_received_date = buyer_received_date
        self.seller_client_order_id = seller_client_order_id
        self.seller_company_id = seller_company_id
        self.seller_received_date = seller_received_date

    @classmethod
    def from_buy_and_sell_order(cls, executed_quantity, executed_price, buy_order, sell_order,
                                execution_time):
        """
        Args:
            executed_quantity (float): quantity of the order execution
            executed_price (float): the price on which both parties execute order
            buy_order (TradingClass.Order):
            sell_order (TradingClass.Order):
            execution_time (TradingClass.FIXDateTimeUTC)
        """
        order_execution = cls(execution_id=None, quantity=executed_quantity, price=executed_price,
                              execution_time=execution_time,
                              buyer_client_order_id=buy_order.client_order_id,
                              buyer_company_id=buy_order.account_company_id,
                              buyer_received_date=buy_order.received_date,
                              seller_client_order_id=sell_order.client_order_id,
                              seller_company_id=sell_order.account_company_id,
                              seller_received_date=sell_order.received_date)
        return order_execution

    @classmethod
    def create_dummy_order_execution(cls, execution_id=0, quantity=100., price=50.,
                                     execution_time=FIXDateTimeUTC.from_date_fix_time_stamp_string(
                                         "20111111-11:11:11"),
                                     buyer_client_order_id="client",
                                     buyer_company_id="Client Firm",
                                     buyer_received_date=FIXDate.from_fix_date_stamp_string("20111110"),
                                     seller_client_order_id="MS",
                                     seller_company_id="Morgan Stanely",
                                     seller_received_date=FIXDate.from_fix_date_stamp_string("20111109")):
        """
        Args:
            executed_quantity (float): quantity of the order execution
            executed_price (float): the price on which both parties execute order
            buy_order (TradingClass.Order):
            sell_order (TradingClass.Order):
            execution_time (TradingClass.FIXDateTimeUTC)
        """
        dummy_order_execution = cls(execution_id, quantity, price, execution_time, buyer_client_order_id,
                                    buyer_company_id, buyer_received_date, seller_client_order_id,
                                    seller_company_id, seller_received_date)
        return dummy_order_execution

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(self, other)

    @property
    def buyer_order_id(self):
        """
        Returns:
             buyer_order_id (string):
        """
        return Order.create_order_id(self.buyer_client_order_id, self.buyer_company_id,
                                     self.buyer_received_date)

    @property
    def seller_order_id(self):
        """
        Returns:
             seller_order_id (string):
        """
        return Order.create_order_id(self.seller_client_order_id, self.seller_company_id,
                                     self.seller_received_date)


class OrderCancel(object):
    """Constructor of class OrderCancel, it is designed after the OrderCancel table from the database
    Args:
        orginal_client_order_id= The order ID from the client side to be cancelled
        client_order_id (string): The cancelled order ID from the client side
        account_company_id (string): account company id related to the order
        stock_ticker (string): ticker symbol of the stock referring in the order
        side = side (int)
        order_quantity = order quantity (int)
        last_status = last status (int)
        msg_seq_num = message sequence number (int)
        on_behalf_of_company_id = original sender who sends order (String)
        sender_sub_id = sub identifier of sender (String)

    """

    def __init__(self, client_order_id, order_cancel_id, account_company_id, order_received_date, stock_ticker,
                 side,
                 order_quantity, last_status, received_time, msg_seq_num=None, on_behalf_of_company_id=None,
                 sender_sub_id=None, cancel_quantity=None, execution_time=None):
        self.client_order_id = client_order_id
        self.order_cancel_id = order_cancel_id
        self.account_company_id = account_company_id
        self.order_received_date = order_received_date
        self.stock_ticker = stock_ticker
        self.side = side
        self.order_quantity = order_quantity
        self.last_status = last_status
        self.received_time = received_time
        self.msg_seq_num = msg_seq_num
        self.on_behalf_of_company_id = on_behalf_of_company_id
        self.sender_sub_id = sender_sub_id
        self.cancel_quantity = cancel_quantity
        self.execution_time = execution_time

    @classmethod
    def from_order_cancel_request(cls, order_cancel_request):
        """Creates a order from a TradingClass.OrderCancelRequest
        Args:
            order_cancel_request (TradingClass.OrderCancelRequest):
        Returns:
            order_cancel (TradingClass.OrderCancel): The order cancel object
        """

        client_order_id = order_cancel_request.orig_cl_ord_id
        order_cancel_id = order_cancel_request.cl_ord_id
        account_company_id = order_cancel_request.sender_comp_id
        order_received_date = None
        received_time = FIXDateTimeUTC.create_for_current_time()
        stock_ticker = order_cancel_request.symbol
        side = order_cancel_request.side
        order_quantity = order_cancel_request.order_qty
        last_status = DatabaseHandlerUtils.LastStatus.PENDING
        message_sequence_number = None
        on_behalf_of_company_id = None
        sender_sub_id = None
        cancel_quantity = None
        execution_time = None
        order_cancel = cls(client_order_id, order_cancel_id, account_company_id, order_received_date, stock_ticker,
                           side, order_quantity, last_status, received_time, message_sequence_number,
                           on_behalf_of_company_id, sender_sub_id, cancel_quantity, execution_time)
        return order_cancel


###########################
### GUI related classes ###
###########################

class StockInformation():
    def __init__(self, p_price, p_high, p_low):
        self.price = p_price
        self.high = p_high
        self.low = p_low


class StockHistory():
    def __init__(self, p_time, p_price, p_quantity):
        """ A stock history object to be represented

        Args:
            p_time (list of string):  YYYY-MM-DD-HH-MM
            p_price (list of float):
            p_quantity (list of int): quantities
        """
        self.time = p_time
        self.price = p_price
        self.quantity = p_quantity


class OrderBookBuy():
    def __init__(self, p_price, p_quantity):
        # price,quantity are list type, with length of 5
        self.price = p_price
        self.quantity = p_quantity


class OrderBookSell():
    def __init__(self, p_price, p_quantity):
        # price,quantity are list type, with length of 5
        self.price = p_price
        self.quantity = p_quantity


class MarketData():
    def __init__(self, p_stock_information, p_stock_history, p_order_book_buy, p_order_book_sell):
        # type of parameters:
        # stock_information -> StockInformation
        # stock_history -> StockHistory
        # order_book_buy -> OrderBookBuy
        # order_book_sell -> OrderBookSell
        self.stock_information = p_stock_information
        self.stock_history = p_stock_history
        self.order_book_buy = p_order_book_buy
        self.order_book_sell = p_order_book_sell


class TradingTransaction():
    def __init__(self, p_time, p_price, p_quantity, p_side):
        # side: True means buy, False means sell
        self.time = p_time
        self.price = p_price
        self.quantity = p_quantity
        self.side = p_side
