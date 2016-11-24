# -*- coding: utf-8 -*-
import MySQLdb

#Said to Alex: When you think this code is ok, you can replace test_client.cfg with client.cfg
file_out=open("test_client.cfg","w")

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='FSCDatabase',port=3306)
    cur=conn.cursor()
    cur.execute("select * from Account")
    results=cur.fetchall()
    conn.close()

    outString="# copy of http://stackoverflow.com/questions/35983928/how-to-send-fix-message-with-quickfix-j\
                \n[DEFAULT]\
                \nApplicationID=client\
                \nConnectionType=initiator\
                \nFileStorePath=storage/client_messages\
                \nFileLogPath=log/client_log\
                \nStartTime=00:01:00\
                \nEndTime=23:59:00\
                \nHeartBtInt=30\
                \nSocketAcceptPort=5520\
                \nUseDataDictionary=Y\
                \nDataDictionary=spec/FIX42.xml\
                \nValidateUserDefinedFields=N\
                \nValidateIncomingMessage=N\
                \nRefreshOnLogon=Y\
                \nValidateUserDefinedFields=N\
                \nResetOnLogon=Y\
                \n#ResetOnLogout=Y\
                \n#HttpAcceptPort=9911\
                \n#ReconnectInterval=60\
                \n\n\n# standard config elements"
    for row in results:
        outString=outString+"\n\n[SESSION]\
                                \n# inherit ConnectionType, ReconnectInterval and SenderCompID from default\
                                \nBeginString=FIX.4.2\
                                \nSenderCompID="+row[0]+"\
                                \nTargetCompID=server\
                                \nSocketConnectHost=localhost\
                                \nSocketConnectPort=5501"

    file_out.write(outString)



except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
