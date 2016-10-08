# -*- coding: utf-8 -*-
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='FSC',port=3306)
    cur=conn.cursor()
    cur.execute("insert into User(phone,name,password) values('18800000000','test','test')")
    conn.commit()
    conn.close()


except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])