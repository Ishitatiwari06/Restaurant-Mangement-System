-- 	Views
-- 1: Customer Order Summary
CREATE VIEW CustomerOrderSummary AS
SELECT
    O.OrderID,
    C.CustomerName,
    O.OrderDate,
    O.TotalAmount,
    O.Status
FROM Orders O
JOIN Customers C
ON O.CustomerID = C.CustomerID;
SELECT * FROM CustomerOrderSummary;

-- 2: Menu with Category
CREATE VIEW MenuCategoryView AS
SELECT
    M.ItemName,
    C.CategoryName,
    M.Price,
    M.Availability
FROM MenuItems M
JOIN Categories C
ON M.CategoryID = C.CategoryID;
SELECT * FROM MenuCategoryView;

-- 3: Payment Report
CREATE VIEW PaymentReport AS
SELECT
    P.PaymentID,
    C.CustomerName,
    P.PaymentMethod,
    P.PaymentStatus,
    P.PaymentDate
FROM Payments P
JOIN Orders O
ON P.OrderID = O.OrderID
JOIN Customers C
ON O.CustomerID = C.CustomerID;
SELECT * FROM PaymentReport;

-- 4: Sales Summary
CREATE VIEW SalesSummary AS
SELECT
    DATE(OrderDate) AS SalesDate,
    COUNT(OrderID) AS TotalOrders,
    SUM(TotalAmount) AS TotalRevenue
FROM Orders
GROUP BY DATE(OrderDate);

SELECT * FROM SalesSummary;

-- 2: Stored Procedures
-- 1: Get Customer Orders
DELIMITER $$

CREATE PROCEDURE GetCustomerOrders(IN CustID INT)
BEGIN
    SELECT
        OrderID,
        OrderDate,
        TotalAmount
    FROM Orders
    WHERE CustomerID = CustID;
END$$

DELIMITER ;
CALL GetCustomerOrders(1);

-- 2: Get Menu by Category
DELIMITER $$

CREATE PROCEDURE GetMenuByCategory(IN CatID INT)
BEGIN
    SELECT
        ItemName,
        Price
    FROM MenuItems
    WHERE CategoryID = CatID;
END$$

DELIMITER ;
CALL GetMenuByCategory(2);

-- 3: Get Total Revenue
DELIMITER $$

CREATE PROCEDURE GetTotalRevenue()
BEGIN
    SELECT
        SUM(TotalAmount) AS TotalRevenue
    FROM Orders;
END $$

DELIMITER ;

CALL GetTotalRevenue();

-- 3: Top Selling Items
DELIMITER $$

CREATE PROCEDURE GetTopSellingItems()
BEGIN
    SELECT
        M.ItemName,
        SUM(OD.Quantity) AS QuantitySold
    FROM MenuItems M
    JOIN OrderDetails OD
        ON M.ItemID = OD.ItemID
    GROUP BY M.ItemID, M.ItemName
    ORDER BY QuantitySold DESC
    LIMIT 5;
END $$

DELIMITER ;

CALL GetTopSellingItems();

-- 3: Triggers
-- 1: Prevent Negative Prices
DELIMITER $$

CREATE TRIGGER CheckMenuPrice
BEFORE INSERT ON MenuItems
FOR EACH ROW
BEGIN
    IF NEW.Price <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price must be greater than zero';
    END IF;
END$$

DELIMITER ;
INSERT INTO MenuItems
(ItemName, CategoryID, Price)
VALUES
('Invalid Food',1,-100);

-- 2. Auto-update Order table
DELIMITER $$

CREATE TRIGGER UpdateOrderTotal
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Orders
    SET TotalAmount =
    (
        SELECT SUM(Subtotal)
        FROM OrderDetails
        WHERE OrderID = NEW.OrderID
    )
    WHERE OrderID = NEW.OrderID;
END $$

DELIMITER ;
INSERT INTO Orders
(CustomerID, EmployeeID, TableID)
VALUES
(1,3,1);

INSERT INTO OrderDetails
(OrderID, ItemID, Quantity, Subtotal)
VALUES
(LAST_INSERT_ID(),6,2,640);

SELECT OrderID, TotalAmount
FROM Orders
ORDER BY OrderID DESC
LIMIT 1;

-- 4: Indexes
-- Index on Customer Phone
CREATE INDEX idx_customer_phone
ON Customers(Phone);
-- Index on Menu Item Name
CREATE INDEX idx_item_name
ON MenuItems(ItemName);
-- Index on Order Date
CREATE INDEX idx_order_date
ON Orders(OrderDate);
-- 4: Index on Customer ID in Orders
CREATE INDEX idx_order_customer
ON Orders(CustomerID);
SHOW INDEX FROM Customers;
SHOW INDEX FROM Orders;

-- 5: Transactions
START TRANSACTION;

UPDATE MenuItems
SET Price = Price + 20
WHERE CategoryID = 2;

SAVEPOINT PriceUpdated;

UPDATE Employees
SET Salary = Salary + 1000
WHERE Role = 'Waiter';

ROLLBACK TO PriceUpdated;

COMMIT;