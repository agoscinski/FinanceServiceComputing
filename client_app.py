import sys
import quickfix as fix
import quickfix44 as fix44
from datetime import datetime
import pdb


class ClientFIXApplication(fix.Application):
    def __init__(self, client_fix_handler, user_id, password):
        self.client_fix_handler = client_fix_handler
        self.user_id = user_id
        self.password = password
        super(ClientFIXApplication, self).__init__()

    def onCreate(self, session_id):
        print ("Application created - session: " + session_id.toString())

    def onLogon(self, session_id):
        print "Logon", session_id

    def onLogout(self, session_id):
        print "Logout", session_id

    def toAdmin(self, message, session_id):
        msg_type = message.getHeader().getField(fix.MsgType())
        if msg_type.getString() == fix.MsgType_Logon:
            self.client_fix_handler.handle_logon_request(message)
        # if Logon request
        # send username and password
        # then flush it


    def fromAdmin(self, message, session_id):
        pass

    def fromApp(self, message, session_id):
        self.onMessage(message, session_id)
        print "IN", message

    def toApp(self, message, session_id):
        print "OUT", message

    def _calculate_checksum(self):
        pass

    def get_user_id(self):
        return self.user_id

    def get_password(self):
        return self.password

    def del_user_id(self):
        del self.user_id

    def del_password(self):
        del self.password


class ClientFIXHandler():
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
        self.client_config_file_name = client_config_file_name
        self.fix_application = None
        self.socket_initiator = None
        self.storeFactory = None
        self.logFactory = None

    def init_fix_settings(self, user_id, password, default_client_config_file_name=None):
        client_config_file_name = self.client_config_file_name if default_client_config_file_name is None else default_client_config_file_name
        settings = fix.SessionSettings(client_config_file_name)
        self.fix_application = ClientFIXApplication(self, user_id, password)
        self.storeFactory = fix.FileStoreFactory(settings)
        self.logFactory = fix.ScreenLogFactory(settings)
        self.socket_initiator = fix.SocketInitiator(self.fix_application, self.storeFactory, settings, self.logFactory)

    def send_logon_request(self, user_id, password):
        self.init_fix_settings(user_id, password)
        self.socket_initiator.start()
        return

    def handle_logon_request(self, message):
        message.setField(fix.RawData(self.fix_application.get_password()))
        message.setField(fix.RawDataLength(len(self.fix_application.get_password())))
        message.getHeader().setField(fix.SenderSubID(self.fix_application.get_user_id()))
        #TODO recalculate checksum
        #message.getHeader().setField(fix.BodyLength(200))
        #message.getHeader().setField(fix.CheckSum(3))
        #self.fix_application.del_user_id()
        #self.fix_application.del_password()

    def send_logout_request(self):
        self.socket_initiator.stop()


class ClientLogic():
    def __init__(self, client_config_file_name):
        self.client_fix_handler = ClientFIXHandler(self, client_config_file_name)
        self.gui_handler = GUIHandler(self)

    def start_client(self):
        # start some gui stuff and other things, for now only
        self.gui_handler.start_gui()

    def logon(self, user_id, password):
        self.client_fix_handler.send_logon_request(user_id, password)


class GUIHandler():
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        while True:
            print '''input 1 to logon\ninput 2 to quit'''
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
        self.client_logic.logon(user_id, password)

