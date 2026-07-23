-- SQL Queries
-- Part A: Basic Queries
-- 1. Display all customers
SELECT * FROM Customers;
-- 2. Display all menu items
SELECT * FROM MenuItems;
-- 3. Show only available food items
SELECT *
FROM MenuItems
WHERE Availability='Available';
-- 4. Display employees working as Waiters
SELECT *
FROM Employees
WHERE Role='Waiter';
-- 5. Display menu items costing more than ₹200
SELECT ItemName, Price
FROM MenuItems
WHERE Price > 200;
-- 6. Sort menu by price (Highest First)
SELECT ItemName, Price
FROM MenuItems
ORDER BY Price DESC;
-- 7. Display first five menu items
SELECT *
FROM MenuItems
LIMIT 5;
-- 8. Find customers whose name starts with 'A'
SELECT *
FROM Customers
WHERE CustomerName LIKE 'A%';
-- 9. Find menu items containing "Pizza"
SELECT *
FROM MenuItems
WHERE ItemName LIKE '%Pizza%';
-- 10. Display unique employee roles
SELECT DISTINCT Role
FROM Employees;

-- Part B: Aggregate Functions
-- 11. Count total customers
SELECT COUNT(*) AS TotalCustomers
FROM Customers;
-- 12. Average food price
SELECT AVG(Price) AS AveragePrice
FROM MenuItems;
-- 13. Maximum food price
SELECT MAX(Price) AS HighestPrice
FROM MenuItems;
-- 14. Minimum food price
SELECT MIN(Price) AS LowestPrice
FROM MenuItems;
-- 15. Total salary of employees
SELECT SUM(Salary) AS TotalSalary
FROM Employees;

-- Part C: GROUP BY
-- 16. Number of employees in each role
SELECT Role,
       COUNT(*) AS TotalEmployees
FROM Employees
GROUP BY Role;
-- 17. Average salary by role
SELECT Role,
       AVG(Salary) AS AverageSalary
FROM Employees
GROUP BY Role;
-- 18. Number of menu items in each category
SELECT CategoryID,
       COUNT(*) AS TotalItems
FROM MenuItems
GROUP BY CategoryID;
-- 19. Total sales by payment method
SELECT PaymentMethod,
       COUNT(*) AS TotalPayments
FROM Payments
GROUP BY PaymentMethod;
-- 20. Customers having more than one order
SELECT CustomerID,
       COUNT(*) AS OrdersPlaced
FROM Orders
GROUP BY CustomerID
HAVING COUNT(*) > 1;

-- Part D: Joins
-- 21. Show customer names with their orders
SELECT
C.CustomerName,
O.OrderID,
O.TotalAmount
FROM Customers C
INNER JOIN Orders O
ON C.CustomerID = O.CustomerID;
-- 22. Show food items with category names
SELECT
M.ItemName,
C.CategoryName,
M.Price
FROM MenuItems M
INNER JOIN Categories C
ON M.CategoryID = C.CategoryID;
-- 23. Show complete order details
SELECT
O.OrderID,
C.CustomerName,
E.EmployeeName,
R.TableID,
O.TotalAmount
FROM Orders O
JOIN Customers C
ON O.CustomerID=C.CustomerID
JOIN Employees E
ON O.EmployeeID=E.EmployeeID
JOIN RestaurantTables R
ON O.TableID=R.TableID;
-- 24. Display every ordered food item
SELECT
O.OrderID,
M.ItemName,
OD.Quantity,
OD.Subtotal
FROM OrderDetails OD
JOIN MenuItems M
ON OD.ItemID=M.ItemID
JOIN Orders O
ON OD.OrderID=O.OrderID;
-- 25. Payment details with customer names
SELECT
C.CustomerName,
P.PaymentMethod,
P.PaymentStatus
FROM Payments P
JOIN Orders O
ON P.OrderID=O.OrderID
JOIN Customers C
ON O.CustomerID=C.CustomerID;
-- Part E: Subqueries
-- 26. Most expensive menu item
SELECT *
FROM MenuItems
WHERE Price =
(
SELECT MAX(Price)
FROM MenuItems
);
-- 27. Customers spending above average
SELECT *
FROM Orders
WHERE TotalAmount >
(
SELECT AVG(TotalAmount)
FROM Orders
);
-- 28. Employees earning more than average salary
SELECT *
FROM Employees
WHERE Salary >
(
SELECT AVG(Salary)
FROM Employees
);
-- 29. Second highest salary
SELECT MAX(Salary)
FROM Employees
WHERE Salary <
(
SELECT MAX(Salary)
FROM Employees
);
-- 30. Customers who never placed an order
SELECT *
FROM Customers
WHERE CustomerID NOT IN
(
SELECT CustomerID
FROM Orders
);
-- Part F: CASE Statement
31. Categorize menu items by price
SELECT
ItemName,
Price,
CASE
WHEN Price < 100 THEN 'Cheap'
WHEN Price BETWEEN 100 AND 300 THEN 'Medium'
ELSE 'Expensive'
END AS PriceCategory
FROM MenuItems;

-- Part G: Common Table Expression (CTE)
-- 32. Orders above average amount
WITH AvgSales AS
(
SELECT AVG(TotalAmount) AvgAmount
FROM Orders
)

SELECT *
FROM Orders
WHERE TotalAmount >
(
SELECT AvgAmount
FROM AvgSales
);

-- Part H: Window Functions
-- 33. Rank employees by salary
SELECT
EmployeeName,
Salary,
RANK() OVER(ORDER BY Salary DESC) AS SalaryRank
FROM Employees;
-- 34. Dense Rank
SELECT
EmployeeName,
Salary,
DENSE_RANK() OVER(ORDER BY Salary DESC) AS DenseRank
FROM Employees;
-- 35. Row Number
SELECT
EmployeeName,
Salary,
ROW_NUMBER() OVER(ORDER BY Salary DESC) AS RowNum
FROM Employees;
-- 36. Running total of sales
SELECT
OrderDate,
TotalAmount,
SUM(TotalAmount)
OVER(ORDER BY OrderDate) AS RunningSales
FROM Orders;
-- 37. Previous order amount
SELECT
OrderID,
TotalAmount,
LAG(TotalAmount)
OVER(ORDER BY OrderID) AS PreviousOrder
FROM Orders;
-- 38. Next order amount
SELECT
OrderID,
TotalAmount,
LEAD(TotalAmount)
OVER(ORDER BY OrderID) AS NextOrder
FROM Orders;

-- Part I: Business Reports
-- 39. Top 5 selling food items
SELECT
M.ItemName,
SUM(OD.Quantity) AS TotalSold
FROM OrderDetails OD
JOIN MenuItems M
ON OD.ItemID=M.ItemID
GROUP BY M.ItemName
ORDER BY TotalSold DESC
LIMIT 5;
-- 40. Total revenue
SELECT
SUM(TotalAmount) AS TotalRevenue
FROM Orders;