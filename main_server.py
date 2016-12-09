import sys
import quickfix as fix
import server

try:
    application_id = "main"
    server = server.ServerLogic(application_id)
    server.start_server()
except fix.ConfigError, e:
    print e