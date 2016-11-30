CREATE VIEW `PendingBuyOrderCurrentQuantity` AS
SELECT PendingBuyOrder.Stock_Ticker, OrderExecution.Order_BuyClientOrderID, OrderExecution.Order_BuyCompanyID, OrderExecution.Order_BuyReceivedDate, PendingBuyOrder.OrderQuantity - SUM(OrderExecution.OrderExecutionQuantity) AS CurrentBuyQuantity 
FROM 
	(SELECT * FROM `Order` WHERE Order.Side = 1 AND Order.LastStatus = 1) PendingBuyOrder 
INNER JOIN 
	OrderExecution
ON PendingBuyOrder.ClientOrderID = OrderExecution.Order_BuyClientOrderID AND PendingBuyOrder.Account_CompanyID = OrderExecution.Order_BuyCompanyID AND PendingBuyOrder.ReceivedDate = OrderExecution.Order_BuyReceivedDate
GROUP BY PendingBuyOrder.ClientOrderID, PendingBuyOrder.Account_CompanyID, PendingBuyOrder.ReceivedDate
ORDER BY PendingBuyOrder.Stock_Ticker;


CREATE VIEW `PendingSellOrderCurrentQuantity` AS
SELECT PendingSellOrder.Stock_Ticker, OrderExecution.Order_SellClientOrderID, OrderExecution.Order_SellCompanyID, OrderExecution.Order_SellReceivedDate, PendingSellOrder.OrderQuantity- SUM(OrderExecution.OrderExecutionQuantity) AS CurrentSellQuantity 
FROM 
	(SELECT * FROM `Order` WHERE Order.Side = 2 AND Order.LastStatus = 1) PendingSellOrder 
INNER JOIN 
	OrderExecution
ON PendingSellOrder.ClientOrderID = OrderExecution.Order_SellClientOrderID AND PendingSellOrder.Account_CompanyID = OrderExecution.Order_SellCompanyID AND PendingSellOrder.ReceivedDate = OrderExecution.Order_SellReceivedDate
GROUP BY PendingSellOrder.ClientOrderID, PendingSellOrder.Account_CompanyID, PendingSellOrder.ReceivedDate
ORDER BY PendingSellOrder.Stock_Ticker;



CREATE VIEW `PendingOrderCurrentQuantity` AS
SELECT pending_buy.Ticker, (pending_buy.CurrentBuyQuantity + pending_sell.CurrentSellQuantity) AS CurrentQuantity
FROM 
	(SELECT Stock.Ticker, IFNULL(CurrentBuyQuantity, 0) AS CurrentBuyQuantity FROM Stock LEFT JOIN PendingBuyOrderCurrentQuantity ON Stock.Ticker = PendingBuyOrderCurrentQuantity.Stock_Ticker) pending_buy
INNER JOIN
	(SELECT Stock.Ticker, IFNULL(CurrentSellQuantity, 0) AS CurrentSellQuantity FROM Stock LEFT JOIN PendingSellOrderCurrentQuantity ON Stock.Ticker = PendingSellOrderCurrentQuantity.Stock_Ticker) pending_sell
ON pending_buy.Ticker = pending_sell.Ticker;



CREATE VIEW `LastExecutedTradeTime` AS
SELECT Order.Stock_Ticker, MAX(OrderExecution.ExecutionTime) AS LastExecutedTradeTime
FROM 
	`Order` 
INNER JOIN
	OrderExecution 
ON Order.ClientOrderID = OrderExecution.Order_BuyClientOrderID AND Order.Account_CompanyID = OrderExecution.Order_BuyCompanyID AND Order.ReceivedDate = OrderExecution.Order_BuyReceivedDate
GROUP BY Order.Stock_Ticker;


CREATE VIEW `CurrentPrice` AS
SELECT order_execution.Stock_Ticker, CAST(100*(order_execution.OrderExecutionPrice / order_execution.OrderExecutionQuantity) AS UNSIGNED) AS CurrentPrice
FROM 
	LastExecutedTradeTime
INNER JOIN
	(SELECT Order.Stock_Ticker, OrderExecution.ExecutionTime, OrderExecution.OrderExecutionPrice, OrderExecution.OrderExecutionQuantity FROM `Order` INNER JOIN OrderExecution ON Order.ClientOrderID = OrderExecution.Order_BuyClientOrderID AND Order.Account_CompanyID = OrderExecution.Order_BuyCompanyID AND Order.ReceivedDate = OrderExecution.Order_BuyReceivedDate) order_execution
ON LastExecutedTradeTime.Stock_Ticker = order_execution.Stock_Ticker
WHERE LastExecutedTradeTime.LastExecutedTradeTime = order_execution.ExecutionTime;


CREATE VIEW `OrderCumulativeQuantityAndAveragePrice` AS
SELECT `Order`.ClientOrderID, `Order`.Account_CompanyID, `Order`.ReceivedDate, IFNULL(grouped_order_execution.CumulativeQuantity,0), IFNULL(grouped_order_execution.AveragePrice,0)
FROM
	((SELECT Order_BuyClientOrderID AS ClientOrderID, Order_BuyCompanyID AS CompanyID, Order_BuyReceivedDate AS ReceivedDate, SUM(OrderExecutionQuantity) AS CumulativeQuantity, AVG(OrderExecutionPrice) AS AveragePrice
	FROM OrderExecution
	GROUP BY Order_BuyClientOrderID, Order_BuyCompanyID, Order_BuyReceivedDate)
	UNION
	(SELECT Order_SellClientOrderID  AS ClientOrderID, Order_SellCompanyID AS CompanyID, Order_SellReceivedDate AS ReceivedDate, SUM(OrderExecutionQuantity) AS CumulativeQuantity, AVG(OrderExecutionPrice) AS AveragePrice
	FROM OrderExecution
	GROUP BY Order_SellClientOrderID, Order_SellCompanyID, Order_SellReceivedDate)) grouped_order_execution
RIGHT OUTER JOIN
	`Order`
ON `Order`.ClientOrderID = grouped_order_execution.ClientOrderID AND `Order`.Account_CompanyID = grouped_order_execution.CompanyID AND `Order`.ReceivedDate = grouped_order_execution.ReceivedDate;
-- merge for buy and sell
-- join with order
