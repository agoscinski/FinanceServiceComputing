# -*- coding: utf-8 -*-
import MySQLdb


class ClientConfigFileHandler():
    def __init__(self, file_name=None, application_id="client", connection_type="initiator",
                 file_store_path="storage/client_messages", file_log_path="log/client_log", start_time="08:00:00",
                 end_time="17:00:00", heart_bt_int="30",
                 socket_accept_port="5520", use_data_dictionary="Y", data_dictionary="spec/FIX42.xml",
                 validate_user_defined_fields="N", validate_incoming_message="N",
                 refresh_on_logon="Y", reset_on_logon="Y", reset_on_logout="Y",
                 http_accept_port="9911", reconnect_interval="60", begin_string="FIX.4.2",
                 target_comp_id="server", socket_connect_host="localhost",
                 socket_connect_port="5501"):
        self.file_name = "client_" + application_id + ".cfg"
        self.application_id = application_id
        self.connection_type = connection_type
        self.file_store_path = file_store_path
        self.file_log_path = file_log_path
        self.start_time = start_time
        self.end_time = end_time
        self.heart_bt_int = heart_bt_int
        self.socket_accept_port = socket_accept_port
        self.use_data_dictionary = use_data_dictionary
        self.data_dictionary = data_dictionary
        self.validate_user_defined_fields = validate_user_defined_fields
        self.validate_incoming_message = validate_incoming_message
        self.refresh_on_logon = refresh_on_logon
        self.reset_on_logon = reset_on_logon
        self.reset_on_logout = reset_on_logout
        self.http_accept_port = http_accept_port
        self.reconnect_interval = reconnect_interval

        self.begin_string = begin_string
        self.target_comp_id = target_comp_id
        self.socket_connect_host = socket_connect_host
        self.socket_connect_port = socket_connect_port
        # TODO the rest attributes

    def create_config_file(self):
        with open(self.file_name, "w") as client_cfg:
            outString = "[DEFAULT]\
                        \nApplicationID=" + self.application_id + "\
                        \nConnectionType=" + self.connection_type + "\
                        \nFileStorePath=" + self.file_store_path + "\
                        \nFileLogPath=" + self.file_log_path + "\
                        \nStartTime=" + self.start_time + "\
                        \nEndTime=" + self.end_time + "\
                        \nHeartBtInt=" + self.heart_bt_int + "\
                        \nSocketAcceptPort=" + self.socket_accept_port + "\
                        \nUseDataDictionary=" + self.use_data_dictionary + "\
                        \nDataDictionary=" + self.data_dictionary + "\
                        \nValidateUserDefinedFields=" + self.validate_user_defined_fields + "\
                        \nValidateIncomingMessage=" + self.validate_incoming_message + "\
                        \nRefreshOnLogon=" + self.refresh_on_logon + "\
                        \nResetOnLogon=" + self.reset_on_logon + "\
                        \n#ResetOnLogout=" + self.reset_on_logout + "\
                        \n#HttpAcceptPort=" + self.http_accept_port + "\
                        \n#ReconnectInterval=" + self.reconnect_interval + "\
                        \n\n\n# standard config elements\
                        \n\n[SESSION]\
                        \n# inherit ConnectionType, ReconnectInterval and SenderCompID from default\
                        \nBeginString=" + self.begin_string + "\
                        \nSenderCompID=" + self.application_id + "\
                        \nTargetCompID=" + self.target_comp_id + "\
                        \nSocketConnectHost=" + self.socket_connect_host + "\
                        \nSocketConnectPort=" + self.socket_connect_port + ""

            client_cfg.write(outString)
            return self.file_name


class ServerConfigFileHandler():
    def __init__(self, file_name=None, application_id="server", connection_type="acceptor",
                 file_store_path="storage/server_messages", file_log_path="log/server_log", start_time="08:00:00",
                 end_time="17:00:00", heart_bt_int="30",
                 socket_accept_port="5520", use_data_dictionary="Y", data_dictionary="spec/FIX42.xml",
                 validate_user_defined_fields="N", validate_incoming_message="N",
                 refresh_on_logon="Y", reset_on_logon="Y", reset_on_logout="Y",
                 http_accept_port="9911", reconnect_interval="60", begin_string="FIX.4.2",
                 target_comp_id="client", socket_connect_host="localhost",
                 socket_connect_port="5501"):
        self.file_name = "server_"+application_id+".cfg"
        self.application_id = application_id
        self.connection_type = connection_type
        self.file_store_path = file_store_path
        self.file_log_path = file_log_path
        self.start_time = start_time
        self.end_time = end_time
        self.heart_bt_int = heart_bt_int
        self.socket_accept_port = socket_accept_port
        self.use_data_dictionary = use_data_dictionary
        self.data_dictionary = data_dictionary
        self.validate_user_defined_fields = validate_user_defined_fields
        self.validate_incoming_message = validate_incoming_message
        self.refresh_on_logon = refresh_on_logon
        self.reset_on_logon = reset_on_logon
        self.reset_on_logout = reset_on_logout
        self.http_accept_port = http_accept_port
        self.reconnect_interval = reconnect_interval

        self.begin_string = begin_string
        self.target_comp_id = target_comp_id
        self.sender_comp_id = application_id
        self.socket_connect_host = socket_connect_host
        self.socket_connect_port = socket_connect_port
        # TODO the rest attributes

    def create_config_file(self, database_handler):
        """
        Args:
            database_handler (TradingClass.DatabaseHandler)
        """
        with open(self.file_name, "w") as client_cfg:
            try:
                conn = MySQLdb.connect(host=database_handler.database_host, user=database_handler.user_name,
                                       passwd=database_handler.user_password, db=database_handler.database_name,
                                       port=database_handler.database_port)
                cur = conn.cursor()
                cur.execute("select * from Account")
                results = cur.fetchall()
                conn.close()

                outString = "[DEFAULT]\
                            \nBeginString=" + self.begin_string + "\
                            \nApplicationID=" + self.application_id + "\
                            \nConnectionType=" + self.connection_type + "\
                            \nFileStorePath=" + self.file_store_path + "\
                            \nFileLogPath=" + self.file_log_path + "\
                            \nStartTime=" + self.start_time + "\
                            \nEndTime=" + self.end_time + "\
                            \nHeartBtInt=" + self.heart_bt_int + "\
                            \nSocketAcceptPort=" + self.socket_accept_port + "\
                            \nSenderCompID = " + self.sender_comp_id +"\
                            \nUseDataDictionary=" + self.use_data_dictionary + "\
                            \nDataDictionary=" + self.data_dictionary + "\
                            \nValidateUserDefinedFields=" + self.validate_user_defined_fields + "\
                            \nValidateIncomingMessage=" + self.validate_incoming_message + "\
                            \nRefreshOnLogon=" + self.refresh_on_logon + "\
                            \nResetOnLogon=" + self.reset_on_logon + "\
                            \n#ResetOnLogout=" + self.reset_on_logout + "\
                            \n#HttpAcceptPort=" + self.http_accept_port + "\
                            \n#ReconnectInterval=" + self.reconnect_interval + "\
                            \n\n\n# standard config elements"
                for row in results:
                    outString = outString + "\n\n[SESSION]\
                                            \nTargetCompID=" + row[0] + ""

                client_cfg.write(outString)
                return self.file_name
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
