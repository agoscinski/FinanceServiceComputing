#
Python coding guidelines: https://www.python.org/dev/peps/pep-0008/
Documentation style demo: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
#Installation
##Database

###mysql version: 5.7.15
Install Mysql on ubuntu: 
  use "sudo apt-get install mysql-client mysql-server" command in Terminal of Ubuntu

###python version:2.7.12

###library used: MySQL-python-1.2.5
Install library: 
   1) sudo apt-get install libmysqlclient-dev
   2) sudo pip install MySQL-python  (you need to make sure that pip is installed)


##htmlPy

1) Installing python package manager: pip
```
sudo apt-get install python-pip
```

2) Installing htmlPy
```
pip install htmlPy
```

3) Installing PySide
```
sudo apt-get install python-pyside
```
4) Installing jinja2, which is depended by htmlPy.
```
sudo pip install jinja2
```

5) Installing PyQt4
```
sudo apt-get install python-qt4
```

## Pytest
```
pip install -U pytest
```

#Demo
##Database
###Prepare:
Create database "FSC":
  1) use "mysql -u root -p" command to open mysql client in Terminal
  2) use "create datebase FSC" command in mysql client
  
###Create table in FSC:
```python
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
```

###Insert
```python
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
```

###Query
```python
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
```
##Pytest
After you created the database
```
py.test test_server.py
```
