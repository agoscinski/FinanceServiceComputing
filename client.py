import sys
import client_app as app

client_config_file_name = sys.argv[1] if len(sys.argv) == 2 else "client.cfg"
client = app.ClientLogic(client_config_file_name)
client.start_client()

