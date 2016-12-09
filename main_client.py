import client
import sys

appication_id = sys.argv[1] if len(sys.argv) == 2 else "client"
client = client.ClientLogic(appication_id)
client.start_client()