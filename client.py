import sys
import os
import time
import thread
import quickfix as fix
import quickfix44 as fix44
from datetime import datetime
import client_app as app


fileName = sys.argv[1] if len(sys.argv) == 2 else "client.cfg"
settings = fix.SessionSettings (fileName)
application = app.Application ()
storeFactory = fix.FileStoreFactory (settings)
logFactory = fix.ScreenLogFactory (settings)
initiator = fix.SocketInitiator (application, storeFactory, settings, logFactory)

initiator.start ()
application.run ()
initiator.stop ()


