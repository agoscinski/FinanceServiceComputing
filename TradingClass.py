import datetime


class MarketDataRequest(object):
    """Constructor of class MarketDataRequest:
        @Parameter:
            md_req_id : market data request IDD (string)
            subscription_request_type : Type of subscription of market data request (char)
            market_depth : market depth of market data request (int)
            no_md_entry_types : number of market data entry requested (int)
            md_entry_type_list : list of market data entries (int)
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

    "return market data request ID"

    def get_md_req_id(self):
        return self.md_req_id

    "return subscription request type "

    def get_subscription_request_type(self):
        return self.subscription_request_type

    "return market depth (top or full or N tier market depth)"

    def get_market_depth(self):
        return self.market_depth

    "return number of market data entry requested"

    def get_no_md_entry_types(self):
        return self.no_md_entry_types

    "return list of md entry requested"

    def get_md_entry_type_list(self):
        return self.md_entry_type_list

    "return number of symbol requested"

    def get_no_related_symbol(self):
        return self.no_related_symbol

    "return list of symbol requested"

    def get_symbol_list(self):
        return self.symbol_list

    "return symbol from list of symbol in i index requested"

    def get_symbol(self, i):
        return self.symbol_list[i]

    "set market data request ID"

    def set_md_req_id(self, md_req_id):
        self.md_req_id = md_req_id

    "set subscription request type "

    def set_subscription_request_type(self, subscription_request_type):
        self.subscription_request_type = subscription_request_type

    "set market depth (top or full or N tier market depth)"

    def set_market_depth(self, market_depth):
        self.market_depth = market_depth

    "set number of market data entry requested"

    def set_no_md_entry_types(self, no_md_entry_types):
        self.no_md_entry_types = no_md_entry_types

    "set list of md entry requested"

    def set_md_entry_type_list(self, md_entry_type_list):
        self.md_entry_type_list = md_entry_type_list

    "set number of symbol requested"

    def set_no_related_symbol(self, no_related_symbol):
        self.no_related_symbol = no_related_symbol

    "set list of symbol requested"

    def set_symbol_list(self, symbol_list):
        self.symbol_list = symbol_list

    def set_symbol(self, i, symbol):
        self.symbol_list[i] = symbol


class MarketDataResponse(object):
    """Constructor of class MarketDataResponse:
        @Parameter:
            md_req_id : market data response ID related to market data request ID (string)
            no_md_entry_types = no_md_entry_types (int)
            symbol = symbol (string)
            md_entry_type_list = md entry type list (list of char)
            md_entry_px_list = md entry price list (list of float)
            md_entry_size_list = md entry size list (list of float)
            md_entry_date_list = md entry date list (list of DateFix Object=> datetime UTC Date YYYYMMDD)
            md_entry_time_list = md entry time list (list of TimeFix Object=> datetime UTC Time HH:MM:SS)
    """

    def __init__(self, md_req_id, no_md_entry_types, symbol, md_entry_type_list, md_entry_px_list,
                 md_entry_size_list, md_entry_date_list, md_entry_time_list):
        self.md_req_id = md_req_id

        self.no_md_entry_types = no_md_entry_types
        self.symbol = symbol
        self.md_entry_type_list = md_entry_type_list
        self.md_entry_px_list = md_entry_px_list
        self.md_entry_size_list = md_entry_size_list
        self.md_entry_date_list = md_entry_date_list
        self.md_entry_time_list = md_entry_time_list

    "return market data request ID"

    def get_md_req_id(self):
        return self.md_req_id

    "return number of market data entries response"

    def get_no_md_entry_types(self):
        return self.no_md_entry_types

    "return symbol requested"

    def get_symbol(self):
        return self.symbol

    "return list of market data entries"

    def get_md_entry_type_list(self):
        return self.md_entry_type_list

    "return list of market data price"

    def get_md_entry_px_list(self):
        return self.md_entry_px_list

    "return list of market data entry size"

    def get_md_entry_size_list(self):
        return self.md_entry_size_list

    "return list of market data entry date"

    def get_md_entry_date_list(self):
        return self.md_entry_date_list

    "return list of market data entry time"

    def get_md_entry_time_list(self):
        return self.md_entry_time_list

    "return a market data entry at index i"

    def get_md_entry_type(self, i):
        return self.md_entry_type_list[i]

    "return a market data price at index i"

    def get_md_entry_px(self, i):
        return self.md_entry_px_list[i]

    "return a market data entry size at index i"

    def get_md_entry_size(self, i):
        return self.md_entry_size_list[i]

    "return a market data entry date at index i"

    def get_md_entry_date(self, i):
        return self.md_entry_date_list[i]

    "return a market data entry time at index i"

    def get_md_entry_time(self, i):
        return self.md_entry_time_list[i]

    "set market data request ID"

    def set_md_req_id(self, md_req_id):
        self.md_req_id = md_req_id

    "set number of market data entries response"

    def set_no_md_entry_types(self, no_md_entry_types):
        self.no_md_entry_types = no_md_entry_types

    "set a symbol"

    def set_symbol(self, symbol):
        self.symbol = symbol

    "set list of market data entries"

    def set_md_entry_type_list(self, md_entry_type_list):
        self.md_entry_type_list = md_entry_type_list

    "set list of market data price"

    def set_md_entry_px_list(self, md_entry_px_list):
        self.md_entry_px_list = md_entry_px_list

    "set list of market data entry size"

    def set_md_entry_size_list(self, md_entry_size_list):
        self.md_entry_size_list = md_entry_size_list

    "set list of market data entry date"

    def set_md_entry_date_list(self, md_entry_date_list):
        self.md_entry_date_list = md_entry_date_list

    "set list of market data entry time"

    def set_md_entry_time_list(self, md_entry_time_list):
        self.md_entry_time_list = md_entry_time_list


class FixOrder(object):
    """Constructor of class FixOrder:
        @Parameter:
        cl_ord_id = client order id (String)
        handl_inst = handling instruction (char)
        exec_inst= execution instruction (String)
        symbol = symbol (String)
        side = side (char)
        maturity_month_year = maturity month year (YearMonthFix Object=> datetime Date with format YYYYMM)
        maturity_day = maturity day (int 1-31)
        transact_time = transaction time (DateTimeFix Object=> DateTime datetime UTC YYYYMMDD-HH:MM:SS)
        order_qty = order quantity (float)
        ord_type = order type (char)
        price = price (float)
        stop_px = stop price (float)
    """

    def __init__(self, cl_ord_id, handl_inst, exec_inst, symbol, maturity_month_year, maturity_day, side, transact_time
                 , order_qty, ord_type, price, stop_px, sender_comp_id, sending_time, on_behalf_of_comp_id
                 , sender_sub_id):
        self.cl_ord_id = cl_ord_id
        self.handl_inst = handl_inst
        self.exec_inst = exec_inst
        self.symbol = symbol
        self.maturity_month_year = maturity_month_year
        self.maturity_day = maturity_day
        self.side = side
        self.transact_time = transact_time
        self.order_qty = order_qty
        self.ord_type = ord_type
        self.price = price
        self.stop_px = stop_px
        self.sender_comp_id = sender_comp_id
        self.sending_time = sending_time
        self.on_behalf_of_comp_id = on_behalf_of_comp_id
        self.sender_sub_id = sender_sub_id

    "return client order id"

    def get_cl_ord_id(self):
        return self.cl_ord_id

    "return handling institution"

    def get_handl_inst(self):
        return self.handl_inst

    "return execution instruction"

    def get_exec_inst(self):
        return self.exec_inst

    "return symbol"

    def get_symbol(self):
        return self.symbol

    "return maturity month year"

    def get_maturity_month_year(self):
        return self.maturity_month_year

    "return maturity day"

    def get_maturity_day(self):
        return self.maturity_day

    "return side buy/sell"

    def get_side(self):
        return self.side

    "return transaction time"

    def get_transact_time(self):
        return self.transact_time

    "return order quantity"

    def get_order_qty(self):
        return self.order_qty

    "return order type"

    def get_ord_type(self):
        return self.ord_type

    "return order price"

    def get_price(self):
        return self.price

    "return order stop price"

    def get_stop_px(self):
        return self.stop_px

    "return sender company id of order "

    def get_sender_comp_id(self):
        return self.sender_comp_id

    "return sending time of order"

    def get_sending_time(self):
        return self.sending_time

    "return original sender company of order "

    def get_on_behalf_of_comp_id(self):
        return self.on_behalf_of_comp_id

    "return additional sender id"

    def get_sender_sub_id(self):
        return self.sender_sub_id

    "set client order id"

    def set_cl_ord_id(self, cl_ord_id):
        self.cl_ord_id = cl_ord_id

    "set handling institution"

    def set_handl_inst(self, handl_inst):
        self.handl_inst = handl_inst

    "set execution instruction"

    def set_exec_inst(self, exec_inst):
        self.exec_inst = exec_inst

    "set symbol"

    def set_symbol(self, symbol):
        self.symbol = symbol

    "set maturity month year"

    def set_maturity_month_year(self, maturity_month_year):
        self.maturity_month_year = maturity_month_year

    "set maturity day"

    def set_maturity_day(self, maturity_day):
        self.maturity_day = maturity_day

    "set side buy/sell"

    def set_side(self, side):
        self.side = side

    "set transaction time"

    def set_transact_time(self, transact_time):
        self.transact_time = transact_time

    "set order quantity"

    def set_order_qty(self, order_qty):
        self.order_qty = order_qty

    "set order type"

    def set_ord_type(self, ord_type):
        self.ord_type = ord_type

    "set order price"

    def set_price(self, price):
        self.price

    "set order stop price"

    def set_stop_px(self, stop_px):
        self.stop_px = stop_px

    "set sender company id of order "

    def set_sender_comp_id(self, sender_comp_id):
        self.sender_comp_id = sender_comp_id

    "set sending time of order"

    def set_sending_time(self, sending_time):
        self.sending_time = sending_time

    "set original sender company of order "

    def set_on_behalf_of_comp_id(self, on_behalf_of_comp_id):
        self.on_behalf_of_comp_id = on_behalf_of_comp_id

    "set additional sender id"

    def set_sender_sub_id(self, sender_sub_id):
        self.sender_sub_id = sender_sub_id


class OrderExecution(object):
    """Constructor of class FixOrder:
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

    def __init__(self, order_id, cl_ord_id, exec_id, exec_trans_type, exec_type, ord_status, symbol, side, leaves_qty
                 , cum_qty, avg_px, price, stop_px):
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

    "return order id "

    def get_order_id(self):
        return self.order_id

    "return client order id"

    def get_cl_ord_id(self):
        return self.cl_ord_id

    "return execution id"

    def get_exec_id(self):
        return self.exec_id

    "return execution transaction type"

    def get_exec_trans_type(self):
        return self.exec_trans_type

    "return execution type"

    def get_exec_type(self):
        return self.exec_type

    "return order status"

    def get_ord_status(self):
        return self.ord_status

    "return symbol"

    def get_symbol(self):
        return self.symbol

    "return side buy/sell"

    def get_side(self):
        return self.side

    "return quantity leaves to be fulfiled"

    def get_leaves_qty(self):
        return self.leaves_qty

    "return cumulative quantity"

    def get_cum_qty(self):
        return self.cum_qty

    "return average price"

    def get_avg_px(self):
        return self.avg_px

    "return price"

    def get_price(self):
        return self.price

    "return stop price"

    def get_stop_px(self):
        return self.stop_px

    "set order id "

    def set_order_id(self):
        return self.order_id

    "set client order id"

    def set_cl_ord_id(self, cl_ord_id):
        self.cl_ord_id = cl_ord_id

    "set execution id"

    def set_exec_id(self, exec_id):
        self.exec_id = exec_id

    "set execution transaction type"

    def set_exec_trans_type(self, exec_trans_type):
        self.exec_trans_type = exec_trans_type

    "set execution type"

    def set_exec_type(self, exec_type):
        self.exec_type = exec_type

    "set order status"

    def set_ord_status(self, ord_status):
        self.ord_status = ord_status

    "set symbol"

    def set_symbol(self, symbol):
        self.symbol = symbol

    "set side buy/sell"

    def set_side(self, side):
        self.side = side

    "set quantity leaves to be fulfiled"

    def set_leaves_qty(self, leaves_qty):
        self.leaves_qty = leaves_qty

    "set cumulative quantity"

    def set_cum_qty(self, cum_qty):
        self.cum_qty = cum_qty

    "set average price"

    def set_avg_px(self, avg_px):
        self.avg_px = avg_px

    "set price"

    def set_price(self, price):
        self.price = price

    "set stop price"

    def set_stop_px(self, stop_px):
        self.stop_px = stop_px


class YearMonthFix(object):
    """Constructor of YearMonthFix
        @Parameter:
            year : year in int
            month: month in int
    """

    def __init__(self, year, month):
        self.month_year = datetime.date(year, month, 1)

    def get_year_month(self):
        return self.month_year

    def __str__(self):
        return self.month_year.strftime("%Y%m")

    def set_year_month(self, year, month):
        self.month_year = datetime.date(year, month, 1)

    def set_year_month_string(self, string):
        self.month_year = datetime.datetime.strptime(string, "%Y%m").date()

    def set_year_month_value(self, date):
        self.month_year = date


class DateFix(object):
    """Constructor of YearMonthFix
        @Parameter:
            year : year in int
            month: month in int
            date: date in int
    """

    def __init__(self, year, month, date):
        self.date = datetime.date(year, month, date)

    def get_date(self):
        return self.date

    def __str__(self):
        return self.date.strftime("%Y%m%d")

    def set_date(self, year, month, date):
        self.date = datetime.date(year, month, date)

    def set_date_string(self, string):
        self.date = datetime.datetime.strptime(string, "%Y%m%d").date()

    def set_date_value(self, date):
        self.date = date


class TimeFix(object):
    """Constructor of TimeFix
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


class DateTimeUTCFix(object):
    """Constructor of DateTimeFix
        @Parameter:
            year : year in int
            month : month in int
            date : date in int
            hour : hour in int
            minute : minutes in int
            second : second in int
    """

    def __init__(self, year, month, date, hour, minute, second):
        self.date_time = datetime.datetime(year, month, date, hour, minute, second, 0)

    def get_date_time(self):
        return self.date_time

    def __str__(self):
        return self.date_time.strftime("%Y%m%d-%H:%M:%S")

    def set_date_time(self, year, month, date, hour, minute, second):
        self.date_time = datetime.datetime(year, month, date, hour, minute, second, 0)

    def set_date_time_string(self, string):
        self.date_time = datetime.datetime.strptime(string, "%Y%m%d-%H:%M:%S").date()

    def set_date_time_default_string(self, string):
        self.date_time = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").date()

    def set_date_time_value(self, date_time):
        self.date_time = date_time

    def set_date_time_now(self):
        self.date_time = datetime.datetime.utcnow()


class Order(object):
    """Constructor of class Order:
        @Parameter:
        client_order_id = client order id (String)
        account_company_id= account company id related to the order (String)
        received_time = received time (DateTimeFix Object=> DateTime datetime UTC YYYYMMDD-HH:MM:SS)
        handling_instruction = handling instruction (char)
        symbol = symbol (String)
        side = side (char)
        order_type = order type (char)
        order_quantity = order quantity (float)
        price = price (float)
        last_status = last status (int)
        msg_seq_num = message sequence number (int)
        on_behalf_of_company_id = original sender who sends order (String)
        sender_sub_id = sub identifier of sender (String)
        cash_order_quantity = amount of order requested (float)
    """

    def __init__(self, client_order_id, account_company_id, received_time, handling_instruction, stock_ticker, side,
                 order_type, order_quantity, price, last_status, msg_seq_num, on_behalf_of_company_id, sender_sub_id,
                 cash_order_quantity):
        self.client_order_id = client_order_id
        self.account_company_id = account_company_id
        self.received_time = received_time
        self.handling_instruction = handling_instruction
        self.stock_ticker = stock_ticker
        self.side = side
        self.order_type = order_type
        self.order_quantity = order_quantity
        self.price = price
        self.last_status = last_status
        self.msg_seq_num = msg_seq_num
        self.on_behalf_of_company_id = on_behalf_of_company_id
        self.sender_sub_id = sender_sub_id
        self.cash_order_quantity = cash_order_quantity

    "return client order id"

    def get_client_order_id(self):
        return self.client_order_id

    "return account company id"

    def get_account_company_id(self):
        return self.account_company_id

    "return received time"

    def get_received_time(self):
        return self.received_time

    "return handling instruction"

    def get_handling_instruction(self):
        return self.handling_instruction

    "return stock ticker"

    def get_stock_ticker(self):
        return self.stock_ticker

    "return side buy/sell"

    def get_side(self):
        return self.side

    "return order type"

    def get_order_type(self):
        return self.order_type

    "return order quantity"

    def get_order_quantity(self):
        return self.order_quantity

    "return order price"

    def get_price(self):
        return self.price

    "return last status of order"

    def get_last_status(self):
        return self.last_status

    "return message sequence number of order"

    def get_msg_seq_num(self):
        return self.msg_seq_num

    "return on behalf of company in order"

    def get_on_behalf_of_company_id(self):
        return self.on_behalf_of_company_id

    "return sender sub id in order"

    def get_sender_sub_id(self):
        return self.sender_sub_id

    "return cash order quantity"

    def get_cash_order_quantity(self):
        return self.cash_order_quantity

    "set client order id"

    def set_client_order_id(self):
        self.client_order_id

    "set account company id"

    def set_account_company_id(self):
        self.account_company_id

    "set received time"

    def set_received_time(self):
        self.received_time

    "set handling instruction"

    def set_handling_instruction(self):
        self.handling_instruction

    "set stock_tickers"

    def set_stock_ticker(self, stock_ticker):
        self.stock_ticker = stock_ticker

    "set side buy/sell"

    def set_side(self, side):
        self.side = side

    "set order type"

    def set_order_type(self, order_type):
        self.order_type = order_type

    "set order quantity"

    def set_order_quantity(self, order_quantity):
        self.order_quantity = order_quantity

    "set order price"

    def set_price(self, price):
        self.price = price

    "set last status of order"

    def set_last_status(self, last_status):
        self.last_status = last_status

    "set message sequence number of order"

    def set_msg_seq_num(self, msg_seq_num):
        self.msg_seq_num = msg_seq_num

    "set on behalf of company in order"

    def set_on_behalf_of_company_id(self, on_behalf_of_company_id):
        self.on_behalf_of_company_id = on_behalf_of_company_id

    "set sender sub id in order"

    def set_sender_sub_id(self, sender_sub_id):
        self.sender_sub_id = sender_sub_id

    "set cash order quantity"

    def set_cash_order_quantity(self, cash_order_quantity):
        self.cash_order_quantity = cash_order_quantity

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
        # time,price,quantity are list type
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
