import sys
import quickfix as fix
import pdb
import htmlPy
import json
sys.path.append('GUI')
from frontEnd import htmlPy_app

class GUISignal(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.

    def __init__(self,g):
        super(GUISignal,self).__init__()
        self.gui_handler=g
        # Initialize the class here, if required.
        return

    @htmlPy.Slot(str,str,result=str)
    def logIn(self,usr,psw):
        #login
        usr=str(usr)
        psw=str(psw)
        print usr,psw
        if(self.gui_handler.button_login_actuated(usr,psw)):
            return_message='{"success":true,"userName":"'+usr+'"}'
        else:
            return_message='{"success":false,"msg":"username or password is wrong"}'
        return return_message

    @htmlPy.Slot()
    def logOut(self):
        self.gui_handler.button_logout_actuated()


    @htmlPy.Slot(str, result=str)
    def get_form_data(self, json_data):
        # @htmlPy.Slot(arg1_type, arg2_type, ..., result=return_type)
        # This function can be used for GUI forms.
        #
        form_data = json.loads(json_data)
        print form_data
        print json.dumps(form_data)
        return json.dumps(form_data)

    @htmlPy.Slot()
    def javascript_function(self):
        # Any function decorated with @htmlPy.Slot decorater can be called
        # using javascript in GUI
        return

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

        #TODO block mechanism
        self.block_gui()

        return self.succes

        #Notice that we should validate here
        return True

    def block_gui(self):
        pass

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

    def request_trading_transactions(self, user_name):
        #TODO alex write database request/fetch
        #TODO FIRST yelinsheng sample data
        trading_transaction = None
        return trading_transaction


class GUIHandler:
    def __init__(self, client_logic):
        self.client_logic = client_logic
        pass

    def start_gui(self):
        # here the gui stuff should be started, for now console
        while(True):
            print '''input 1 to run in terminal\ninput 2 to start gui\ninput 3 to quit'''
            input = raw_input()
            #input='2'
            if(input=='1'):
                self.wait_for_input()
            elif(input=='2'):
                file=open("rawData.json","r")
                rawData=file.read()
                json={
                    "rawData":rawData
                }
                htmlPy_app.template = ("index.html", json)
                htmlPy_app.bind(GUISignal(self))
                htmlPy_app.start()
            elif(input=='3'):
                break
            else:
                continue


    def wait_for_input(self):
        while True:
            print '''input 1 to logon\ninput 2 to logout\ninput 3 to quit'''
            input = raw_input()
            if input == '1':
                self.button_login_actuated("john","papapa")
            elif input == '2':
                self.button_logout_actuated()
            elif input == '3':
                break
            else:
                continue

    def button_login_actuated(self, user_name, user_password):
        """This function is activated when the login button is pushed"""
        return self.client_logic.logon(user_name, user_password)


    def request_trading_transactions(self, user_name):
        """Request trading transactions

        Args:
            user_name (string): .

        Returns:
        trading_transactions (string): json string of trading transaction
        """
        trading_transactions = self.client_logic.request_trading_transactions(user_name)
        #TODO yenlinsheng finish this function
        trading_transactions_json = self.extract_trading_transactions_json(trading_transactions)
        pass

    def button_logout_actuated(self):
        """This function is activated when the login button is pushed"""
        respond = self.client_logic.logout()

    def button_buy_actuated(self, stock_ticker, price, quantity):
        #TODO alex
        pass

    def search_for_stock_actuated(self, searching_value):
        """This function is called when the user enters a search request

        Args:
            searching_value (string): The value of the user input

        Returns:
            None
        """
        #TODO alex
        pass

    def refresh_charts(self, market_data):
        #TODO yenlinsheng finish these functions
        quantity_chart_json = self.extract_quantity_chart_json(market_data)
        stock_course_chart_json = self.extract_quantity_chart_json(market_data)
        stock_information_json =  self.extract_stock_information_json(market_data)
        order_book_json = self.extract_order_book_json(market_data)
        pass

    def refresh_trading_transaction_list(self, trading_data):
        #TODO yenlinsheng finish this function
        trading_data_json = self.extract_trading_data_json(trading_data)
        pass

#TODO FIRST yenlinsheng MarketData class
#TODO FIRST yelinsheng TradingTransaction class

client_config_file_name = sys.argv[1] if len(sys.argv) == 2 else "client.cfg"
client = ClientLogic(client_config_file_name)
client.start_client()
