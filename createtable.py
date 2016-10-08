# -*- coding: utf-8 -*-
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='FSC',port=3306)
    cur=conn.cursor()
    cur.execute("DROP TABLE IF EXISTS User")
    cur.execute('create table User(phone char(20),name char(50),password char(50),PRIMARY KEY(phone)) CHARACTER SET = utf8')
    conn.close()


except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
