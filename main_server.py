import sys
import quickfix as fix
import server

try:
    file = sys.argv[1] if len(sys.argv) == 2 else "server.cfg"
    server = server.ServerLogic(file)
    server.start_server()
except fix.ConfigError, e:
    print e