import sys
import quickfix as fix
import quickfix44 as fix44
from datetime import datetime
import pdb

class FIXApplication(fix.Application):

    def onCreate(self, session_id):
        print ("Application created - session: " + session_id.toString())

    def onLogon(self, session_id):
        print "Logon", session_id

    def onLogout(self, session_id):
        print "Logout", session_id

    def toAdmin(self, message, session_id):
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type.getString() == fix.MsgType_Logon:
            self._handle_logon_request(message)
        #if Logon request
        #send username and password
        #then flush it
        pass

    def fromAdmin(self, message, session_id):
        pass

    def fromApp(self, message, session_id):
        self.onMessage(message, session_id)
        print "IN", message

    def toApp(self, message, session_id):
        print "OUT", message

    def _handle_logon_request(self, message):
        message.setField(fix.RawData(self.password))
        message.setField(fix.RawDataLength(sys.getsizeof(self.password)))
        message.setField(fix.SenderSubID(self.user_id))
        #message.getHeader().setField(fix.BodyLength(110))
        del self.user_id
        del self.password

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_password(self, password):
        self.password = password

    def _calculate_checksum(self):
        pass


class ClientFIXHandler():
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
        self.client_config_file_name = client_config_file_name

    def _init_fix_settings(self):
        settings = fix.SessionSettings(self.client_config_file_name)
        self.fix_application = FIXApplication()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.ScreenLogFactory(settings)
        self.socket_initiator = fix.SocketInitiator(self.fix_application, storeFactory, settings, logFactory)

    def send_logon_request(self, user_id, password):
        self._init_fix_settings()
        self.fix_application.set_user_id(user_id)
        self.fix_application.set_password(password)
        self.socket_initiator.start()
        return

    def send_logout_request(self):
        self.initiator.stop()

    def queryEnterOrder(self):
        # example for some functionalities,
        print ("\nTradeCaptureReport (AE)\n")
        trade = fix.Message()
        trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        trade.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReport))

        trade.setField(fix.TradeReportTransType(fix.TradeReportTransType_NEW))  # 487
        # trade.setField (fix.TradeReportID (self.genTradeReportID ()))                  # 571
        trade.setField(fix.TrdSubType(4))  # 829
        trade.setField(fix.SecondaryTrdType(2))  # 855
        trade.setField(fix.Symbol("MYSYMBOL"))  # 55
        trade.setField(fix.LastQty(22))  # 32
        trade.setField(fix.LastPx(21.12))  # 31
        trade.setField(fix.TradeDate((datetime.now().strftime("%Y%m%d"))))  # 75
        # trade.setField (fix.TransactTime ((datetime.now ().strftime ("%Y%m%d-%H:%M:%S.%f"))[:-3]))  # 60
        trade.setField(fix.PreviouslyReported(False))  # 570

        group = fix44.TradeCaptureReport().NoSides()

        group.setField(fix.Side(fix.Side_SELL))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        group.setField(fix.Side(fix.Side_BUY))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        fix.Session.sendToTarget(trade, self.sessionID)

    def genOrderID(self):
        self.current_order_id += 1
        return str(self.cuzrrent_order_id)


class ClientLogic():
    def __init__(self, client_config_file_name):
        self.client_fix_handler = ClientFIXHandler(self, client_config_file_name)
        self.gui_handler = GUIHandler(self)

    def request_logon_information(self):
        user_id, password = self.gui_handler.request_logon_information()
        return user_id, password

    def start_client(self):
        # start some gui stuff and other things, for now only
        self.gui_handler.start_gui()


    def client_logon(self, user_id, password):
        respond = self.client_fix_handler.send_logon_request(user_id, password)
        # handle respond with gui
        return


class GUIHandler():
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        while True:
            print '''
                    input 1 to logon
                    input 2 to quit
                    '''
            input = raw_input()
            print
            if input == '1':
                self.request_logon_information()
            elif input == '2':
                break
            else:
                continue

    def request_logon_information(self):
        user_id = "John"
        password = "hashedpw"
        self.client_logic.client_logon(user_id, password)
        return user_id, password
