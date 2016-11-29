import datetime
import quickfix as fix
import quickfix42 as fix42
from enum import Enum


class MarketDataEntryType(Enum):
    OFFER = 0
    BID = 1
    CURRENT_PRICE = 2
    OPENING_PRICE = 4
    CLOSING_PRICE = 5
    DAY_HIGH = 7
    DAY_LOW = 8


class OrderSideType(Enum):
    BUY = fix.Side_BUY
    SELL = fix.Side_SELL

class OrderType(Enum):
    LIMIT =  fix.TriggerOrderType_LIMIT
    MARKET = fix.TriggerOrderType_MARKET

class LastStatus(Enum):
    DONE = 0
    PENDING = 1
    CANCELED = 2
    EXPIRED = 3

class OrderStatus(Enum):
    NEW = 2
    REPLACED = 3
    PARTIALLY_FILLED = 4
    EXPIRED = 5
    CANCELED = 6
    FILLED = 8
    PENDING_REPLACE = 11
    PENDING_CANCEL = 12


class ExecutionType(Enum):
    NEW = 0
    PARTIAL_FILL = 1
    FILL = 2
    CANCELED = 4
    REJECTED = 8

class ExecutionTransactionType(Enum):
    NEW = '0'
    PARTIAL_FILL = '1'
    FILL = '2'
    CANCELED = '4'
    REPLACE = '5'
    REJECTED = '8'
    EXPIRED = 'C'


# TODO replace with MarketDataEntryType
class MDEntryType:
    TRADE = '2'
    OPENING = '4'
    CLOSING = '5'
    SESSION_HIGH = '7'
    SESSION_LOW = '8'

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
    def from_date_stamp_string(cls, date_stamp_string):
        """Constructor from date stamp strings

        Args:
            date_stamp_string (string): string in format YYYYMMDD
        Returns:
            (FIXDate object)
        """
        date_object = datetime.datetime.strptime(date_stamp_string, "%Y%m%d").date()
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

    def __str__(self):
        return self.date.strftime("%Y%m%d")

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

    def get_time(self):
        return self.time

    def __str__(self):
        return self.time.strftime("%H:%M:%S")

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
    def from_date_time_stamp_string(cls, date_time_stamp_string):
        """Constructor from date stamp strings

        Args:
            date_time_stamp_string (string): string in format YYYYMMDD-HH:MM:SS
        Returns:
            (FIXDate object)
        """
        date_object = datetime.datetime.strptime(date_time_stamp_string, "%Y%m%d-%H:%M:%S").date()
        return cls(date_object)

    def __str__(self):
        return self.date_time.strftime("%Y%m%d-%H:%M:%S")

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


class NewSingleOrder(object):
    """Constructor of class FIXOrder:
        @Parameter:
        client_order_id (string): client order id
        handling_instruction (char): handling instruction
        execution_instruction (string): execution instruction
        symbol (String): symbol of a stock
        maturity_month_year (FIXYearMonth object): the month when the order will mature
        maturity_day (int): maturity day
        side (char): type of order
        transaction_time (FIXDateTimeUTC object): transaction time
        order_quantity (float): order quantity
        order_type (char): order type
        price (float): price
        stop_prices (float): stop price
    """

    def __init__(self, client_order_id, handling_instruction, execution_instruction, symbol, maturity_month_year,
                 maturity_day, side, transaction_time, order_quantity, order_type, price, stop_prices,
                 sender_company_id, sending_time,
                 on_behalf_of_comp_id, sender_sub_id):
        self.client_order_id = client_order_id
        self.handling_instruction = handling_instruction
        self.execution_instruction = execution_instruction
        self.symbol = symbol
        self.maturity_month_year = maturity_month_year
        self.maturity_day = maturity_day
        self.side = side
        self.transaction_time = transaction_time
        self.order_quantity = order_quantity
        self.order_type = order_type
        self.price = price
        self.stop_prices = stop_prices
        self.sender_company_id = sender_company_id
        self.sending_time = sending_time
        self.on_behalf_of_comp_id = on_behalf_of_comp_id
        self.sender_sub_id = sender_sub_id

    @classmethod
    def create_dummy_new_single_order(cls, client_order_id="client", handling_instruction="1", execution_instruction="1",
                                     symbol="TSLA", maturity_month_year=FIXYearMonth.from_year_month(2000, 1), maturity_day=2, side=OrderSideType.BUY,
                                     transaction_time=FIXDateTimeUTC.from_date_time_stamp_string("20000101-10:00:00"), order_quantity=10., order_type=OrderType.LIMIT, price=100.,
                                     stop_prices=None, sender_company_id=None, sending_time=None,
                                     on_behalf_of_company_id=None, sender_sub_id=None):
        """For testing"""
        dummy_new_single_order = cls(client_order_id, handling_instruction, execution_instruction,
                                     symbol, maturity_month_year, maturity_day, side,
                                     transaction_time, order_quantity, order_type, price,
                                     stop_prices, sender_company_id, sending_time,
                                     on_behalf_of_company_id, sender_sub_id)
        return dummy_new_single_order

    @classmethod
    def from_fix_message(cls, fix_message):
        """Constructor from a quickfix.Message"""
        #TODO
        pass

    def get_cl_ord_id(self):
        return self.client_order_id

    def get_handl_inst(self):
        return self.handling_instruction

    def get_exec_inst(self):
        return self.execution_instruction

    def get_symbol(self):
        return self.symbol

    def get_maturity_month_year(self):
        return self.maturity_month_year

    def get_maturity_day(self):
        return self.maturity_day

    def get_side(self):
        return self.side

    def get_transact_time(self):
        return self.transaction_time

    def get_order_qty(self):
        return self.order_quantity

    def get_ord_type(self):
        return self.order_type

    def get_price(self):
        return self.price

    def get_stop_px(self):
        return self.stop_prices

    def get_sender_comp_id(self):
        return self.sender_company_id

    def get_sending_time(self):
        return self.sending_time

    def get_on_behalf_of_comp_id(self):
        return self.on_behalf_of_comp_id

    def get_sender_sub_id(self):
        return self.sender_sub_id

    def set_cl_ord_id(self, cl_ord_id):
        self.client_order_id = cl_ord_id

    def set_handl_inst(self, handl_inst):
        self.handling_instruction = handl_inst

    def set_exec_inst(self, exec_inst):
        self.execution_instruction = exec_inst

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_maturity_month_year(self, maturity_month_year):
        self.maturity_month_year = maturity_month_year

    def set_maturity_day(self, maturity_day):
        self.maturity_day = maturity_day

    def set_side(self, side):
        self.side = side

    def set_transact_time(self, transact_time):
        self.transaction_time = transact_time

    def set_order_qty(self, order_qty):
        self.order_quantity = order_qty

    def set_ord_type(self, ord_type):
        self.order_type = ord_type

    def set_price(self, price):
        self.price

    def set_stop_px(self, stop_px):
        self.stop_prices = stop_px

    def set_sender_comp_id(self, sender_comp_id):
        self.sender_company_id = sender_comp_id

    def set_sending_time(self, sending_time):
        self.sending_time = sending_time

    def set_on_behalf_of_comp_id(self, on_behalf_of_comp_id):
        self.on_behalf_of_comp_id = on_behalf_of_comp_id

    def set_sender_sub_id(self, sender_sub_id):
        self.sender_sub_id = sender_sub_id


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

    def __init__(self, order_id, client_order_id, execution_id, execution_transaction_type, execution_type, order_status, symbol, side, left_quantity
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
    def from_order(cls, order, execution_transaction_type, execution_type, order_status, left_quantity, cumulative_quantity, average_price):
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
        #execution_transaction_type
        #str(execution_type)
        #str(order_status)
        symbol = order.stock_ticker
        side = order.side
        #left_quantity
        #cumulative_quantity
        #average_price
        price = order.price
        execution_report = cls(order_id, client_order_id, execution_id, execution_transaction_type, str(execution_type), str(order_status), symbol, side, left_quantity, cumulative_quantity, average_price, price)
        return execution_report


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
    def __ne__(self, other):
        return  not self.__eq__(self, other)

    def create_fix_message(self):
        """Creates from an execution report a fix message"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_ExecutionReport))
        #header.setField(fix.MsgSeqNum(self.fix_application.exec_id)) TODO? important?
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
        handling_instruction (char): handling instruction
        stock_ticker (string): ticker symbol of the stock referring in the order
        side (int): type of order
        maturity_date (FIXDate object): the date when order will mature
        order_type (char): the type of order, see fix.Side_ for different types
        order_quantity (float): order quantity
        price (float): price of the stock
        last_status (LastStatus): last status
        msg_seq_num (int): message sequence number
        on_behalf_of_company_id (string): original sender who sends order
        sender_sub_id (string): sub identifier of sender
        cash_order_quantity (float): amount of order requested
    """

    def __init__(self, client_order_id, account_company_id, received_date, handling_instruction, stock_ticker, side, maturity_date,
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
    def create_dummy_order(cls, client_order_id="20161120-001", account_company_id="client", received_date=FIXDate.from_date_stamp_string("20161120"), handling_instruction="1",
                          stock_ticker="TSLA", side="1", maturity_date=FIXDate.from_date_stamp_string("20161125"), order_type="1", order_quantity=100.00, price=10.00,
                          last_status=0, msg_seq_num=0):
        """For testing"""
        dummy_order = cls(client_order_id, account_company_id, received_date, handling_instruction,
                          stock_ticker, side, maturity_date, order_type, order_quantity, price,
                          last_status, msg_seq_num)
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
        maturity_date = FIXDate.from_year_month_day(new_single_order.maturity_month_year.year, new_single_order.maturity_month_year.month, new_single_order.maturity_day)
        order_type = new_single_order.order_type
        order_quantity = new_single_order.order_quantity
        price = new_single_order.price
        last_status = LastStatus.PENDING
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
        return  not self.__eq__(self, other)

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


################################
### Database related classes ###
################################


class DatabaseStockInformation:
    def __init__(self, current_price=None, current_volume=None, opening_price=None, closing_price=None, day_high=None,
                 day_low=None):
        self.current_price = current_price
        self.current_volume = current_volume
        self.opening_price = opening_price
        self.closing_price = closing_price
        self.day_high = day_high
        self.day_low = day_low

class OrderExecution:

    def __init__(self, execution_id, quantity, price, execution_time, buyer_client_order_id, buyer_company_id, buyer_received_date, seller_client_order_id, seller_company_id, seller_received_date):
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
    def from_buy_and_sell_order(cls, executed_quantity, executed_price, buy_order, sell_order, execution_time):
        """
        Args:
            executed_quantity (float): quantity of the order execution
            executed_price (float): the price on which both parties execute order
            buy_order (TradingClass.Order):
            sell_order (TradingClass.Order):
            execution_time (TradingClass.FIXDateTimeUTC)
        """
        order_execution = cls(execution_id=0, quantity=executed_quantity, price=executed_price,
                              execution_time=execution_time, buyer_client_order_id=buy_order.client_order_id,
                              buyer_company_id=buy_order.account_company_id, buyer_received_date=buy_order.received_date,
                              seller_client_order_id=sell_order.client_order_id,
                              seller_company_id=sell_order.account_company_id,
                              seller_received_date=sell_order.received_date)
        return order_execution

    @classmethod
    def create_dummy_order_execution(cls, execution_id=0, quantity=100., price=50.,
                           execution_time=FIXDateTimeUTC.from_date_time_stamp_string("20111111-11:11:11"),
                           buyer_client_order_id="client",
                           buyer_company_id="Client Firm",
                           buyer_received_date=FIXDate.from_date_stamp_string("20111110"),
                           seller_client_order_id="MS",
                           seller_company_id="Morgan Stanely",
                           seller_received_date=FIXDate.from_date_stamp_string("20111109")):
        """
        Args:
            executed_quantity (float): quantity of the order execution
            executed_price (float): the price on which both parties execute order
            buy_order (TradingClass.Order):
            sell_order (TradingClass.Order):
            execution_time (TradingClass.FIXDateTimeUTC)
        """
        dummy_order_execution = cls(execution_id, quantity, price, execution_time, buyer_client_order_id, buyer_company_id, buyer_received_date, seller_client_order_id, seller_company_id, seller_received_date, msg_seq_num)
        return dummy_order_execution

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return  not self.__eq__(self, other)
    
    @property
    def buyer_order_id(self):
        """
        Returns:
             buyer_order_id (string):
        """
        return Order.create_order_id(self.buyer_client_order_id, self.buyer_company_id, self.buyer_received_date)
    
    @property
    def seller_order_id(self):
        """
        Returns:
             seller_order_id (string):
        """
        return Order.create_order_id(self.seller_client_order_id, self.seller_company_id, self.seller_received_date)

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
