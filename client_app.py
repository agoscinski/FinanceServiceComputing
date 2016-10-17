import sys
import os
import time
import thread
import quickfix as fix
import quickfix44 as fix44
from datetime import datetime
import cPickle as p


class MinInc(fix.DoubleField):
    def __init__(self, data=None):
        if data == None:
            fix.DoubleField.__init__(self, 6350)
        else:
            fix.DoubleField.__init__(self, 6350, data)


class MinBr(fix.DoubleField):
    def __init__(self, data=None):
        if data == None:
            fix.DoubleField.__init__(self, 6351)
        else:
            fix.DoubleField.__init__(self, 6351, data)


class YTM(fix.DoubleField):
    def __init__(self, data=None):
        if data == None:
            fix.DoubleField.__init__(self, 6360)
        else:
            fix.DoubleField.__init__(self, 6360, data)


class YTW(fix.DoubleField):
    def __init__(self, data=None):
        if data == None:
            fix.DoubleField.__init__(self, 6361)
        else:
            fix.DoubleField.__init__(self, 6361, data)

class Application(fix.Application):

    current_order_id = 0

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        print ("Application created - session: " + sessionID.toString())

    def onLogon(self, sessionID):
        print "Logon", sessionID

    def onLogout(self, sessionID):
        print "Logout", sessionID

    def toAdmin(self, message, sessionID):
        pass

    def fromAdmin(self, message, sessionID):
        pass

    def fromApp(self, message, sessionID):
        self.onMessage(message, sessionID)
        print "IN", message

    def toApp(self, message, sessionID):
        print "OUT", message

    def run(self):
        print '''
        input 1 to send query order,
        input 2 to quit
        input 3 to request market data
        input 4 to make an order
        '''
        while True:
            input = raw_input()

            if input == '1':
                self.queryEnterOrder()
            elif input == '2':
                break
            elif input == '3':
                pass
            else:
                continue

    def logon(self):
        pass

    def queryEnterOrder(self):
        print ("\nTradeCaptureReport (AE)\n")
        trade = fix.Message()
        trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        trade.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReport))

        trade.setField(fix.TradeReportTransType(fix.TradeReportTransType_NEW))  # 487
        # trade.setField (fix.TradeReportID (self.genTradeReportID ()))                  # 571
        trade.setField(fix.TrdSubType(4))  # 829
        trade.setField(fix.SecondaryTrdType(2))  # 855
        trade.setField(fix.Symbol("MYSYMBOL"))  # 55
        trade.setField(fix.LastQty(22))  # 32
        trade.setField(fix.LastPx(21.12))  # 31
        trade.setField(fix.TradeDate((datetime.now().strftime("%Y%m%d"))))  # 75
        # trade.setField (fix.TransactTime ((datetime.now ().strftime ("%Y%m%d-%H:%M:%S.%f"))[:-3]))  # 60
        trade.setField(fix.PreviouslyReported(False))  # 570

        group = fix44.TradeCaptureReport().NoSides()

        group.setField(fix.Side(fix.Side_SELL))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        group.setField(fix.Side(fix.Side_BUY))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        fix.Session.sendToTarget(trade, self.sessionID)

    def genOrderID(self):
        self.current_order_id += 1
        return str(self.current_order_id)
