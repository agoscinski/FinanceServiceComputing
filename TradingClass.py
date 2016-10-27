class MarketDataRequest(object):

    """Constructor of class MarketDataRequest:
        @Parameter:
            mdReqID : market data request IDD (string)
            subscriptionRequestType : Type of subscription of market data request
            marketDepth : market depth of market data request
            mdUpdateType : market data update type
            noMDEntryType : number of market data entry requested
            mdEntries : list of market data entries (int)
            symbols : list of ticker symbol (string)
    """
    def __init__(self, mdReqID, subscriptionRequestType, marketDepth, mdUpdateType, noMDEntryType, mdEntries,
                 symbols):
        self.mdReqID = mdReqID
        self.subscriptionRequestType = subscriptionRequestType
        self.marketDepth = marketDepth
        self.mdUpdateType = mdUpdateType
        self.noMDEntryType = noMDEntryType
        self.mdEntries=mdEntries
        self.symbols=symbols

    "return market data request ID"
    def get_md_req_id(self):
        return self.mdReqID

    "return subscription request type "
    def get_subscription_request_type(self):
        return self.subscriptionRequestType

    "return market depth (top or full or N tier market depth)"
    def get_market_depth(self):
        return self.marketDepth

    "return market data update type"
    def get_md_update_type(self):
        return self.mdUpdateType

    "return number of market data entry requested"
    def get_no_md_entry_type(self):
        return self.noMDEntryType

    "return list of md entry requested"
    def get_md_entries(self):
        return self.mdEntries

    "return list of symbol requested"
    def get_symbols(self):
        return self.symbols

    "return symbol from list of symbol in i index requested"
    def get_symbols(self,i):
        return self.symbols[i]


    "set market data request ID"
    def set_md_req_id(self, mdReqID):
        self.mdReqID = mdReqID

    "set subscription request type "
    def set_subscription_request_type(self, subscriptionRequestType):
        self.subscriptionRequestType = subscriptionRequestType

    "set market depth (top or full or N tier market depth)"
    def set_market_depth(self, marketDepth):
        self.marketDepth = marketDepth

    "set market data update type"
    def set_md_update_type(self, mdUpdateType):
        self.mdUpdateType = mdUpdateType

    "set number of market data entry requested"
    def set_no_md_entry_type(self, noMDEntryType):
        self.noMDEntryType = noMDEntryType

    "set list of md entry requested"
    def set_md_entries(self, mdEntries):
        self.mdEntries = mdEntries

    "set list of symbol requested"
    def set_symbols(self, symbols):
        self.symbols = symbols

    def set_symbols(self,i,symbol):
        self.symbols[i]= symbol


class MarketDataResponse(object):

    """Constructor of class MarketDataResponse:
        @Parameter:
            mdReqID : market data response ID related to market data request ID (string)
            noMDEntries = noMDEntries
            symbol = symbol
            totalVolumeTraded = 0
            mdEntryType = mdEntryType
            mdEntryPx = mdEntryPx
            mdEntrySize = mdEntrySize
            mdEntryTime = mdEntryTime
            currency = currency
            numberOfOrders = numberOfOrders
    """
    def __init__(self, mdReqID, noMDEntries, symbol, totalVolumeTraded, mdEntryType, mdEntryPx, mdEntrySize, mdEntryTime,
                 currency, numberOfOrders):
        self.mdReqID = mdReqID

        self.noMDEntries = noMDEntries
        self.symbol = symbol
        self.totalVolumeTraded = totalVolumeTraded
        self.mdEntryType = mdEntryType
        self.mdEntryPx = mdEntryPx
        self.mdEntrySize = mdEntrySize
        self.mdEntryTime = mdEntryTime
        self.currency = currency
        self.numberOfOrders = numberOfOrders
        #self.securityType = securityType
        #self.maturityMonthYear = maturityMonthYear
        #self.putOrCall = putOrCall
        #self.strikePrice = strikePrice


    "return market data request ID"
    def get_md_req_id(self):
        return self.mdReqID

    "return number of market data entries response"
    def get_no_md_entries(self):
        return self.noMDEntries

    "return list of symbol requested"
    def get_symbol(self):
        return self.symbol

    "return total volume traded for certain stock"
    def get_total_volume_traded(self):
        return self.totalVolumeTraded

    "return list of market data entries"
    def get_md_entry_type(self):
        return self.mdEntryType

    "return list of market data price"
    def get_md_entry_px(self):
        return self.mdEntryPx

    "return list of market data entry size"
    def get_md_entry_size(self):
        return self.mdEntrySize

    "return list of market data entry time"
    def get_md_entry_time(self):
        return self.mdEntryTime

    "return list of market data entry currency"
    def get_currency(self):
        return self.currency

    "return market data entry number of orders"
    def get_number_of_orders(self):
        return self.numberOfOrders

    "set market data request ID"
    def set_md_req_id(self, mdReqID):
        self.mdReqID=mdReqID

    "set number of market data entries response"
    def set_no_md_entries(self, noMDEntries):
        self.noMDEntries=noMDEntries

    "set a symbol"
    def set_symbol(self, symbol):
        self.symbol=symbol

    "set total volume traded for certain stock"
    def set_total_volume_traded(self, totalVolumeTraded):
        self.totalVolumeTraded = totalVolumeTraded

    "set list of market data entries"
    def set_md_entry_type(self, mdEntryType):
        self.mdEntryType = mdEntryType

    "set list of market data price"
    def set_md_entry_px(self, mdEntryPx):
        self.mdEntryPx = mdEntryPx

    "set list of market data entry size"
    def set_md_entry_size(self, mdEntrySize):
        self.mdEntrySize = mdEntrySize

    "set list of market data entry time"
    def set_md_entry_time(self, mdEntryTime):
        self.mdEntryTime = mdEntryTime

    "set list of market data entry currency"
    def set_currency(self, currency):
        self.currency = currency

    "set market data entry number of orders"
    def set_number_of_orders(self, numberOfOrders):
        self.numberOfOrders = numberOfOrders


