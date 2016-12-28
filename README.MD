# Documentation guidelines
Python coding guidelines: https://www.python.org/dev/peps/pep-0008/
Python documentation style demo: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
#Installation
##Requirements

A linux OS, preferable Ubuntu

##Database

###mysql version: 5.7.15
Install Mysql on ubuntu: 
  use "sudo apt-get install mysql-client mysql-server" command in Terminal of Ubuntu

###python version:2.7.12

###library used: MySQL-python-1.2.5
Install library: 
   1) sudo apt-get install libmysqlclient-dev
   2) sudo pip install MySQL-python  (you need to make sure that pip is installed)
###Setting database up
Set username and password to root, otherwise change default variables in ClientLogic.__init__ of ClientDatabaseHandler in client.py and in ServerLogic.__init__ of ServerDatabaseHandler in server.py

##GUI

###htmlPy

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
## Testing

### Pytest
```
pip install -U pytest
```

#Demo

run server with
```
python main_server.py
```
run a client with
```
python main_client.py CLIENT_NAME
```
where possible client names are: "client" and "MS"
