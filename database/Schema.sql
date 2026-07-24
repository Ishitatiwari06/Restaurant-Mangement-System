CREATE DATABASE RestaurantDB;
USE RestaurantDB;

CREATE TABLE Customers
(
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE Employees
(
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeName VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    CHECK (Salary > 0)
);

CREATE TABLE RestaurantTables
(
    TableID INT AUTO_INCREMENT PRIMARY KEY,
    Capacity INT NOT NULL,
    Status ENUM('Available','Occupied') DEFAULT 'Available',
    CHECK (Capacity > 0)
);

CREATE TABLE Categories
(
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE MenuItems
(
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Availability ENUM('Available','Not Available') DEFAULT 'Available',

    CHECK (Price > 0),

    FOREIGN KEY (CategoryID)
        REFERENCES Categories(CategoryID)
);

CREATE TABLE Orders
(
    OrderID INT AUTO_INCREMENT PRIMARY KEY,

    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    TableID INT NOT NULL,

    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,

    TotalAmount DECIMAL(10,2) DEFAULT 0,

    Status ENUM('Pending','Completed')
    DEFAULT 'Pending',

    FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID),

    FOREIGN KEY (EmployeeID)
        REFERENCES Employees(EmployeeID),

    FOREIGN KEY (TableID)
        REFERENCES RestaurantTables(TableID)
);

CREATE TABLE OrderDetails
(
    DetailID INT AUTO_INCREMENT PRIMARY KEY,

    OrderID INT NOT NULL,
    ItemID INT NOT NULL,

    Quantity INT NOT NULL,

    Subtotal DECIMAL(10,2) NOT NULL,

    CHECK (Quantity >= 1),

    FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID)
        ON DELETE CASCADE,

    FOREIGN KEY (ItemID)
        REFERENCES MenuItems(ItemID)
);

CREATE TABLE Payments
(
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,

    OrderID INT UNIQUE,

    PaymentMethod ENUM('Cash','Card','UPI'),

    PaymentStatus ENUM('Paid','Pending')
    DEFAULT 'Pending',

    PaymentDate DATETIME
    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID)
        ON DELETE CASCADE
);

SHOW TABLES;

DESC Customers;
DESC Employees;
DESC RestaurantTables;
DESC Categories;
DESC MenuItems;
DESC Orders;
DESC OrderDetails;
DESC Payments;

INSERT INTO Categories (CategoryName)
VALUES
('Starter'),
('Main Course'),
('Dessert'),
('Beverage');

INSERT INTO RestaurantTables (Capacity, Status)
VALUES
(2,'Available'),
(2,'Available'),
(4,'Available'),
(4,'Occupied'),
(6,'Available'),
(6,'Occupied'),
(8,'Available'),
(4,'Available'),
(2,'Occupied'),
(10,'Available');

INSERT INTO Employees (EmployeeName, Role, Salary)
VALUES
('Rahul Sharma','Manager',50000),
('Priya Singh','Cashier',28000),
('Amit Kumar','Waiter',22000),
('Neha Verma','Waiter',22000),
('Rohan Gupta','Chef',45000),
('Anjali Mehta','Chef',42000),
('Karan Patel','Cleaner',18000),
('Sneha Kapoor','Receptionist',25000),
('Vikas Jain','Waiter',22000),
('Pooja Arora','Cashier',28000);

INSERT INTO Customers (CustomerName, Phone, Email)
VALUES
('Aarav Sharma','9876543210','aarav@gmail.com'),
('Ishita Tiwari','9876543211','ishita@gmail.com'),
('Rohan Singh','9876543212','rohan@gmail.com'),
('Priya Gupta','9876543213','priya@gmail.com'),
('Karan Mehta','9876543214','karan@gmail.com'),
('Ananya Verma','9876543215','ananya@gmail.com'),
('Aditya Kumar','9876543216','aditya@gmail.com'),
('Neha Sharma','9876543217','neha@gmail.com'),
('Mohit Jain','9876543218','mohit@gmail.com'),
('Simran Kaur','9876543219','simran@gmail.com'),
('Aman Patel','9876543220','aman@gmail.com'),
('Pooja Sharma','9876543221','pooja@gmail.com'),
('Rahul Gupta','9876543222','rahul@gmail.com'),
('Sneha Singh','9876543223','sneha@gmail.com'),
('Arjun Kapoor','9876543224','arjun@gmail.com'),
('Ritika Jain','9876543225','ritika@gmail.com'),
('Harsh Verma','9876543226','harsh@gmail.com'),
('Nisha Patel','9876543227','nisha@gmail.com'),
('Deepak Kumar','9876543228','deepak@gmail.com'),
('Kavya Arora','9876543229','kavya@gmail.com');

INSERT INTO MenuItems (ItemName, CategoryID, Price, Availability)
VALUES
('Spring Rolls',1,180,'Available'),
('Paneer Tikka',1,250,'Available'),
('French Fries',1,120,'Available'),
('Veg Manchurian',1,220,'Available'),
('Garlic Bread',1,150,'Available'),

('Paneer Butter Masala',2,320,'Available'),
('Dal Makhani',2,280,'Available'),
('Veg Biryani',2,300,'Available'),
('Chicken Biryani',2,380,'Available'),
('Butter Naan',2,60,'Available'),
('Jeera Rice',2,180,'Available'),
('Fried Rice',2,220,'Available'),
('Hakka Noodles',2,240,'Available'),
('Veg Pizza',2,350,'Available'),
('Chicken Pizza',2,450,'Available'),

('Ice Cream',3,120,'Available'),
('Brownie',3,180,'Available'),
('Gulab Jamun',3,100,'Available'),
('Rasmalai',3,140,'Available'),
('Chocolate Cake',3,220,'Available'),

('Coke',4,60,'Available'),
('Pepsi',4,60,'Available'),
('Lassi',4,90,'Available'),
('Cold Coffee',4,150,'Available'),
('Mango Shake',4,170,'Available'),
('Lemon Soda',4,80,'Available'),
('Orange Juice',4,120,'Available'),
('Mineral Water',4,40,'Available'),
('Tea',4,40,'Available'),
('Coffee',4,70,'Available');

SELECT COUNT(*) AS Categories FROM Categories;
SELECT COUNT(*) AS RestaurantTables FROM RestaurantTables;
SELECT COUNT(*) AS Employees FROM Employees;
SELECT COUNT(*) AS Customers FROM Customers;
SELECT COUNT(*) AS MenuItems FROM MenuItems;

INSERT INTO Orders
(CustomerID,EmployeeID,TableID,OrderDate,TotalAmount,Status)
VALUES
(4,3,5,'2026-02-08 14:47:00',330,'Completed'),
(14,3,1,'2026-01-07 15:32:00',1860,'Completed'),
(15,9,5,'2026-01-25 14:44:00',1090,'Completed'),
(13,3,6,'2026-03-20 16:51:00',900,'Completed'),
(3,9,5,'2026-06-20 17:36:00',450,'Completed'),
(10,3,4,'2026-01-13 16:29:00',2600,'Completed'),
(3,9,3,'2026-05-24 15:10:00',2070,'Completed'),
(11,3,4,'2026-01-26 17:25:00',1340,'Completed'),
(16,4,8,'2026-02-09 14:15:00',1920,'Completed'),
(5,9,8,'2026-01-25 12:55:00',330,'Completed'),
(20,3,7,'2026-04-20 19:33:00',600,'Completed'),
(18,4,6,'2026-01-10 18:10:00',960,'Completed'),
(17,3,5,'2026-06-17 21:12:00',730,'Completed'),
(1,9,6,'2026-04-01 13:59:00',280,'Completed'),
(19,3,2,'2026-06-16 13:48:00',1140,'Completed'),
(14,3,9,'2026-06-23 15:45:00',780,'Completed'),
(4,3,4,'2026-01-11 12:37:00',1620,'Completed'),
(2,4,2,'2026-05-08 16:42:00',1590,'Completed'),
(8,4,7,'2026-02-04 13:42:00',2360,'Completed'),
(4,3,7,'2026-06-11 13:15:00',660,'Completed'),
(6,4,8,'2026-02-28 13:28:00',630,'Completed'),
(16,4,4,'2026-04-02 14:24:00',1240,'Completed'),
(18,9,8,'2026-02-07 16:13:00',570,'Completed'),
(11,3,1,'2026-05-16 20:58:00',1230,'Completed'),
(8,4,2,'2026-05-08 21:38:00',800,'Completed'),
(19,9,6,'2026-03-07 17:15:00',1140,'Completed'),
(3,3,8,'2026-05-19 13:04:00',1420,'Completed'),
(6,4,9,'2026-06-10 21:51:00',1200,'Completed'),
(9,3,2,'2026-06-18 14:17:00',990,'Completed'),
(9,9,8,'2026-03-28 12:05:00',1720,'Completed'),
(6,9,8,'2026-05-23 18:35:00',780,'Completed'),
(2,4,10,'2026-05-05 18:08:00',500,'Completed'),
(8,9,2,'2026-03-25 20:56:00',520,'Completed'),
(1,3,6,'2026-04-26 15:17:00',260,'Completed'),
(16,3,4,'2026-04-12 16:52:00',1080,'Completed'),
(11,4,2,'2026-03-12 20:25:00',1040,'Completed'),
(2,3,10,'2026-04-12 17:27:00',1280,'Completed'),
(14,3,9,'2026-05-22 15:23:00',560,'Completed'),
(4,9,5,'2026-05-10 18:20:00',350,'Completed'),
(13,9,3,'2026-05-19 16:25:00',1800,'Completed');

INSERT INTO OrderDetails
(OrderID,ItemID,Quantity,Subtotal)
VALUES
(1,22,3,180),
(1,24,1,150),
(2,1,3,540),
(2,18,3,300),
(2,7,3,840),
(2,23,2,180),
(3,11,1,180),
(3,9,2,760),
(3,5,1,150),
(4,24,3,450),
(4,15,1,450),
(5,23,1,90),
(5,3,3,360),
(6,27,3,360),
(6,12,2,440),
(6,6,3,960),
(6,7,3,840),
(7,13,3,720),
(7,9,3,1140),
(7,30,3,210),
(8,3,3,360),
(8,7,3,840),
(8,30,2,140),
(9,18,2,200),
(9,9,3,1140),
(9,24,2,300),
(9,19,2,280),
(10,5,1,150),
(10,21,3,180),
(11,18,3,300),
(11,28,3,120),
(11,1,1,180),
(12,1,3,540),
(12,24,2,300),
(12,29,3,120),
(13,12,1,220),
(13,25,3,510),
(14,29,2,80),
(14,27,1,120),
(14,26,1,80),
(15,25,3,510),
(15,5,1,150),
(15,22,2,120),
(15,16,3,360),
(16,13,2,480),
(16,22,2,120),
(16,21,3,180),
(17,8,3,900),
(17,19,3,420),
(17,1,1,180),
(17,3,1,120),
(18,7,3,840),
(18,18,3,300),
(18,5,3,450),
(19,12,3,660),
(19,14,1,350),
(19,15,3,1350),
(20,7,2,560),
(20,18,1,100),
(21,4,1,220),
(21,2,1,250),
(21,21,1,60),
(21,18,1,100),
(22,13,2,480),
(22,9,2,760),
(23,19,3,420),
(23,24,1,150),
(24,6,1,320),
(24,2,1,250),
(24,17,3,540),
(24,3,1,120),
(25,20,2,440),
(25,3,3,360),
(26,13,3,720),
(26,5,2,300),
(26,22,2,120),
(27,7,2,560),
(27,17,1,180),
(27,9,1,380),
(27,5,2,300),
(28,17,3,540),
(28,1,2,360),
(28,22,3,180),
(28,27,1,120),
(29,20,2,440),
(29,7,1,280),
(29,23,3,270),
(30,14,1,350),
(30,27,2,240),
(30,9,1,380),
(30,2,3,750),
(31,4,3,660),
(31,3,1,120),
(32,10,1,60),
(32,12,2,440),
(33,20,1,220),
(33,24,1,150),
(33,5,1,150),
(34,26,1,80),
(34,23,2,180),
(35,8,3,900),
(35,1,1,180),
(36,27,1,120),
(36,18,2,200),
(36,11,1,180),
(36,1,3,540),
(37,17,3,540),
(37,4,1,220),
(37,13,2,480),
(37,29,1,40),
(38,3,2,240),
(38,22,3,180),
(38,30,2,140),
(39,23,1,90),
(39,10,1,60),
(39,18,2,200),
(40,27,2,240),
(40,1,3,540),
(40,10,3,180),
(40,7,3,840);

INSERT INTO Payments
(OrderID,PaymentMethod,PaymentStatus,PaymentDate)
VALUES
(1,'UPI','Paid','2026-02-08 14:47:00'),
(2,'Cash','Paid','2026-01-07 15:32:00'),
(3,'Cash','Paid','2026-01-25 14:44:00'),
(4,'Card','Paid','2026-03-20 16:51:00'),
(5,'Cash','Paid','2026-06-20 17:36:00'),
(6,'UPI','Paid','2026-01-13 16:29:00'),
(7,'Cash','Paid','2026-05-24 15:10:00'),
(8,'Cash','Paid','2026-01-26 17:25:00'),
(9,'Cash','Paid','2026-02-09 14:15:00'),
(10,'Card','Paid','2026-01-25 12:55:00'),
(11,'UPI','Paid','2026-04-20 19:33:00'),
(12,'Cash','Paid','2026-01-10 18:10:00'),
(13,'UPI','Paid','2026-06-17 21:12:00'),
(14,'Cash','Paid','2026-04-01 13:59:00'),
(15,'UPI','Paid','2026-06-16 13:48:00'),
(16,'Card','Paid','2026-06-23 15:45:00'),
(17,'Cash','Paid','2026-01-11 12:37:00'),
(18,'Card','Paid','2026-05-08 16:42:00'),
(19,'UPI','Paid','2026-02-04 13:42:00'),
(20,'Card','Paid','2026-06-11 13:15:00'),
(21,'Card','Paid','2026-02-28 13:28:00'),
(22,'Card','Paid','2026-04-02 14:24:00'),
(23,'UPI','Paid','2026-02-07 16:13:00'),
(24,'UPI','Paid','2026-05-16 20:58:00'),
(25,'UPI','Paid','2026-05-08 21:38:00'),
(26,'Card','Paid','2026-03-07 17:15:00'),
(27,'Card','Paid','2026-05-19 13:04:00'),
(28,'Cash','Paid','2026-06-10 21:51:00'),
(29,'UPI','Paid','2026-06-18 14:17:00'),
(30,'Card','Paid','2026-03-28 12:05:00'),
(31,'UPI','Paid','2026-05-23 18:35:00'),
(32,'Cash','Paid','2026-05-05 18:08:00'),
(33,'Card','Paid','2026-03-25 20:56:00'),
(34,'Cash','Paid','2026-04-26 15:17:00'),
(35,'Card','Paid','2026-04-12 16:52:00'),
(36,'Card','Paid','2026-03-12 20:25:00'),
(37,'UPI','Paid','2026-04-12 17:27:00'),
(38,'UPI','Paid','2026-05-22 15:23:00'),
(39,'UPI','Paid','2026-05-10 18:20:00'),
(40,'Card','Paid','2026-05-19 16:25:00');

SELECT COUNT(*) FROM Orders;
SELECT COUNT(*) FROM OrderDetails;
SELECT COUNT(*) FROM Payments;

