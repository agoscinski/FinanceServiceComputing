import quickfix as fix
import sys
import time
from enum import Enum

class DatabaseRespond(Enum):
	SUCCESS = 0
	FAILURE = 1

class Application(fix.Application):
	orderID = 0
	execID = 0

	#TODO FIX COMMUNICATION
	def onCreate(self, sessionID): return
	def onLogon(self, sessionID): return
	def onLogout(self, sessionID): return
	def toAdmin(self, sessionID, message): return
	def fromAdmin(self, sessionID, message): return
	def toApp(self, sessionID, message): return
	def fromApp(self, message, sessionID):
		print("Received message")
		# contains FIX version
		beginString = fix.BeginString()
		msgType = fix.MsgType()
		message.getHeader().getField( beginString )
		message.getHeader().getField( msgType )
	
		# contains basic information of message
		symbol = fix.Symbol()
		side = fix.Side()
		ordType = fix.OrdType()
		orderQty = fix.OrderQty()
		price = fix.Price()
		clOrdID = fix.ClOrdID()

		# check if msgType is valid
		message.getField( ordType )
		if ordType.getValue() != fix.OrdType_LIMIT:
			raise fix.IncorrectTagValue( ordType.getField() )

		# get basic information of message
		message.getField( symbol )
		message.getField( side )
		message.getField( orderQty )
		message.getField( price )
		message.getField( clOrdID )

		executionReport = fix.Message()
		executionReport.getHeader().setField( beginString )
		executionReport.getHeader().setField( fix.MsgType(fix.MsgType_ExecutionReport) )

		executionReport.setField( fix.OrderID(self.genOrderID()) )
		executionReport.setField( fix.ExecID(self.genExecID()) )
		executionReport.setField( fix.OrdStatus(fix.OrdStatus_FILLED) )
		executionReport.setField( symbol )
		executionReport.setField( side )
		executionReport.setField( fix.CumQty(orderQty.getValue()) )
		executionReport.setField( fix.AvgPx(price.getValue()) )
		executionReport.setField( fix.LastShares(orderQty.getValue()) )
		executionReport.setField( fix.LastPx(price.getValue()) )
		executionReport.setField( clOrdID )
		executionReport.setField( orderQty )

		if beginString.getValue() == fix.BeginString_FIX40 or beginString.getValue() == fix.BeginString_FIX41 or beginString.getValue() == fix.BeginString_FIX42:
			executionReport.setField( fix.ExecTransType(fix.ExecTransType_NEW) )

		if beginString.getValue() >= fix.BeginString_FIX41:
			executionReport.setField( fix.ExecType(fix.ExecType_FILL) )
			executionReport.setField( fix.LeavesQty(0) )

		try:
			fix.Session.sendToTarget( executionReport, sessionID )
		except SessionNotFound as e:
			return

	def genOrderID(self):
		self.orderID = self.orderID+1
		return self.orderID
	def genExecID(self):
		self.execID = self.execID+1
		return self.execID
	
	#TODO SERVER LOGIC
	def process_login_request(self, username, password, timestamp):
		return 0

	def process_ask_request(self, symbol, n_shares):
		return 0 : OrderLogic

	def process_bid_request(self, symbol, n_shares):
		return 0

	def process_stock_request(self):
		return 0
		
	#TODO send SQL Queries
	def send_client_match_query(self):

	def send_add_bid_order_query(self, symbol, price, n_shares, bidder_id):
		#send query
		return DatabaseRespond.SUCCESS

	def send_remove_bid_order_query(self, bidder_id):
		return DatabaseRespond.SUCCESS
	def send_remove_bid_order_query(self, bidder_id, ):
		return DatabaseRespond.SUCCESS
	def request_historic_data(self, timestamp):


	#TODO market simulation
	def request_market(self, symbols):

try:
	file = sys.argv[1] if len(sys.argv) == 2 else "server.cfg"
	settings = fix.SessionSettings(file)
	application = Application()
	storeFactory = fix.FileStoreFactory(settings)
	#logFactory = fix.FileLogFactory(settings)
	logFactory = fix.ScreenLogFactory(settings)
	acceptor = fix.SocketAcceptor(application, storeFactory, settings, logFactory)
	acceptor.start()
	while 1: time.sleep(1)
	#acceptor.stop()
except fix.ConfigError, e:
	print e
