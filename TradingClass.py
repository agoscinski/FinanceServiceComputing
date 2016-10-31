class MarketDataRequest(object):

    """Constructor of class MarketDataRequest:
        @Parameter:
            md_req_id : market data request IDD (string)
            subscription_request_type : Type of subscription of market data request
            market_depth : market depth of market data request
            no_md_entry_types : number of market data entry requested
            md_entry_type_list : list of market data entries (int)
            no_related_sym : number of symbols requested
            symbol_list : list of ticker symbol (string)
    """
    def __init__(self, md_req_id, subscription_request_type, market_depth, no_md_entry_types, md_entry_type_list,
                 no_related_sym,symbol_list):
        self.md_req_id = md_req_id
        self.subscription_request_type = subscription_request_type
        self.market_depth = market_depth
        self.no_md_entry_types = no_md_entry_types
        self.md_entry_type_list=md_entry_type_list
        self.no_related_sym=no_related_sym
        self.symbol_list=symbol_list

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
    def get_symbol(self,i):
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

    "return number of symbol requested"
    def set_no_related_symbol(self,no_related_symbol):
        self.no_related_symbol=no_related_symbol

    "set list of symbol requested"
    def set_symbol_list(self, symbol_list):
        self.symbol_list = symbol_list

    def set_symbol(self,i,symbol):
        self.symbol_list[i]= symbol


class MarketDataResponse(object):

    """Constructor of class MarketDataResponse:
        @Parameter:
            md_req_id : market data response ID related to market data request ID (string)
            no_md_entry_types = no_md_entry_types
            symbol = symbol
            md_entry_type_list = md_entry_type_list
            md_entry_px_list = md_entry_px_list
            md_entry_size_list = md_entry_size_list
            md_entry_date_list = md_entry_date_list
            md_entry_time_list = md_entry_time_list
dl            currency = currency
dl            number_of_orders = number_of_orders
    """
    def __init__(self, md_req_id, no_md_entry_types, symbol, md_entry_type_list, md_entry_px_list,
                 md_entry_size_list, md_entry_time_list, md_entry_date_list):
        self.md_req_id = md_req_id

        self.no_md_entry_types = no_md_entry_types
        self.symbol = symbol
        self.md_entry_type_list = md_entry_type_list
        self.md_entry_px_list = md_entry_px_list
        self.md_entry_size_list = md_entry_size_list
        self.md_entry_date_list= md_entry_date_list
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

    "set market data request ID"
    def set_md_req_id(self, md_req_id):
        self.md_req_id=md_req_id

    "set number of market data entries response"
    def set_no_md_entry_types(self, no_md_entry_types):
        self.no_md_entry_types=no_md_entry_types

    "set a symbol"
    def set_symbol(self, symbol):
        self.symbol=symbol

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

