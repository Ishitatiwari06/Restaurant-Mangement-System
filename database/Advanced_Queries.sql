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

-- 2: Auto-update Table Status
DELIMITER $$

CREATE TRIGGER UpdateTableStatus
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    UPDATE RestaurantTables
    SET Status='Occupied'
    WHERE TableID=NEW.TableID;
END$$

DELIMITER ;
INSERT INTO Orders
(CustomerID, EmployeeID, TableID, TotalAmount)
VALUES
(1,3,2,500);
SELECT * FROM RestaurantTables;

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
SHOW INDEX FROM Customers;

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