import sys
import quickfix as fix
import pdb


class ClientFIXApplication(fix.Application):
    def __init__(self, client_fix_handler):
        self.client_fix_handler = client_fix_handler
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
            self.client_fix_handler.handle_to_be_sent_logon_request(message)

    def fromAdmin(self, message, session_id):
        pass

    def fromApp(self, message, session_id):
        print "IN", message

    def toApp(self, message, session_id):
        print "OUT", message

    def _calculate_checksum(self):
        pass


class ClientFIXHandler():
    def __init__(self, client_logic, client_config_file_name):
        self.client_logic = client_logic
        self.client_config_file_name = client_config_file_name
        self.fix_application = None
        self.socket_initiator = None
        self.storeFactory = None
        self.logFactory = None
        self.user_id = None
        self.password = None

    def init_fix_settings(self, default_client_config_file_name=None):
        client_config_file_name_ = self.client_config_file_name if default_client_config_file_name is None \
            else default_client_config_file_name
        settings = fix.SessionSettings(client_config_file_name_)
        self.fix_application = ClientFIXApplication(self)
        self.storeFactory = fix.FileStoreFactory(settings)
        self.logFactory = fix.FileLogFactory(settings)
        self.socket_initiator = fix.SocketInitiator(self.fix_application, self.storeFactory, settings, self.logFactory)

    def send_logon_request(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def connect_to_server(self, user_id, password):
        self.set_user_id(user_id)
        self.set_password(password)
        self.init_fix_settings()
        self.socket_initiator.start()
        return

    def handle_to_be_sent_logon_request(self, message):
        """Handle a logon request which is about to be sent

        Before the logon request is sent to the server, this function handles the message and modifies fields.

        Args:
            message (Swig Object of type 'FIX::Message *'): the message to be sent
        """
        self.add_user_id_to_message(message)
        self.add_password_to_message(message)
        # TODO @alex flush password
        # self.fix_application.del_user_id()
        # self.fix_application.del_password()

    def send_market_data_request(self):
        """Sends a market data request to server

        TODO @husein description if needed

        Args:
            TODO @husein args

        Returns:

        """
        pass

    def handle_market_data_respond(self, message):
        """Handles market data respond

        TODO @husein description if needed

        Args:
            message (FIX::Message): Market data message to be handled.

        Returns:
            TODO how does the return value look like
        """
        pass

    def add_user_id_to_message(self, message):
        message.setField(fix.RawData(self.get_password()))
        message.setField(fix.RawDataLength(len(self.get_password())))

    def add_password_to_message(self, message):
        message.getHeader().setField(fix.SenderSubID(self.get_user_id()))

    def send_logout_request(self):
        self.socket_initiator.stop()

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_password(self, password):
        self.password = password

    def get_user_id(self):
        return self.user_id

    def get_password(self):
        return self.password

    def del_user_id(self):
        del self.user_id

    def del_password(self):
        del self.password


class ClientLogic():
    def __init__(self, client_config_file_name):
        self.client_fix_handler = ClientFIXHandler(self, client_config_file_name)
        self.gui_handler = GUIHandler(self)

    def start_client(self):
        # start some gui stuff and other things, for now only gui
        self.gui_handler.start_gui()

    def logon(self, user_id, password):
        self.client_fix_handler.connect_to_server(user_id, password)

    def logout(self):
        self.client_fix_handler.send_logout_request()

    def process_market_data_respond(self, message):
        """Process market data respond

        Args:
            message (list of str): .

        Returns:
            None
        """
        return


class GUIHandler:
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        self.wait_for_input()

    def wait_for_input(self):
        while True:
            print '''input 1 to logon\ninput 2 to logout\ninput 3 to quit'''
            input = raw_input()
            if input == '1':
                self.logon_option()
            elif input == '2':
                self.logout_option()
            elif input == '3':
                break
            else:
                continue

    def logon_option(self):
        user_id, password = self.request_logon_information()
        self.client_logic.logon(user_id, password)
        return

    def request_logon_information(self):
        user_id = "John"
        password = "hashedpw"
        return user_id, password

    def logout_option(self):
        respond = self.client_logic.logout()
        # TODO case for failure
        print "Logout successful\n"


client_config_file_name = sys.argv[1] if len(sys.argv) == 2 else "client.cfg"
client = ClientLogic(client_config_file_name)
client.start_client()
