--TODO these are the orders in server database, please add theses ones into the client database of MS
INSERT INTO `Order`(ClientOrderID, Account_CompanyID, ReceivedDate, HandlingInstruction, MaturityDate, Stock_Ticker, Side, OrderType, OrderQuantity, Price, LastStatus) VALUES('0','MS','2016-11-08','1','2016-11-20','TSLA','2','1','100','1200','0');
INSERT INTO `Order`(ClientOrderID, Account_CompanyID, ReceivedDate, HandlingInstruction, MaturityDate, Stock_Ticker, Side, OrderType, OrderQuantity, Price, LastStatus) VALUES('1','MS','2016-11-08','1','2016-11-10', 'TSLA', '2','2','100','100', '0');
INSERT INTO `Order`(ClientOrderID, Account_CompanyID, ReceivedDate, HandlingInstruction, MaturityDate, Stock_Ticker, Side, OrderType, OrderQuantity, Price, LastStatus) VALUES('0','MS','2016-11-09','1','2016-11-20','TSLA','2','2','2000','1010', '1');
INSERT INTO `Order`(ClientOrderID, Account_CompanyID, ReceivedDate, HandlingInstruction, MaturityDate, Stock_Ticker, Side, OrderType, OrderQuantity, Price, LastStatus) VALUES('0','MS','2016-11-09','1','2016-11-15','MS','1','2','10000','1000', '1');
