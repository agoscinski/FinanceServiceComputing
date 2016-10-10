# -*- coding: utf-8 -*-
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='FSC',port=3306)
    cur=conn.cursor()
    cur.execute("select * from User")
    results=cur.fetchall()
    for row in results:
        print "phone=%s,name=%s,password=%s" %(row[0],row[1],row[2])
    conn.close()


except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])