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
    Status ENUM('Available','Occupied')
    DEFAULT 'Available',
    CHECK (Capacity > 0)
);
CREATE TABLE Categories
(
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(50)
    UNIQUE NOT NULL
);
CREATE TABLE MenuItems
(
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    ItemName VARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Availability ENUM('Available','Not Available')
    DEFAULT 'Available',
    CHECK (Price > 0),
    FOREIGN KEY(CategoryID)
    REFERENCES Categories(CategoryID)
);
CREATE TABLE Orders
(
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    TableID INT NOT NULL,
    OrderDate DATETIME
    DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2)
    DEFAULT 0,
    Status ENUM('Pending','Completed')
    DEFAULT 'Pending',
    FOREIGN KEY(CustomerID)
    REFERENCES Customers(CustomerID),
    FOREIGN KEY(EmployeeID)
    REFERENCES Employees(EmployeeID),
    FOREIGN KEY(TableID)
    REFERENCES RestaurantTables(TableID)
);
CREATE TABLE OrderDetails
(
    DetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    ItemID INT NOT NULL,
    Quantity INT NOT NULL,
    Subtotal DECIMAL(10,2) NOT NULL,
    CHECK(Quantity > 0),
    FOREIGN KEY(OrderID)
    REFERENCES Orders(OrderID),
    FOREIGN KEY(ItemID)
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
    FOREIGN KEY(OrderID)
    REFERENCES Orders(OrderID)
);
SHOW TABLES;
DESC Customers;
DESC Orders;
DESC MenuItems;

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

INSERT INTO Orders
(CustomerID, EmployeeID, TableID, TotalAmount, Status)
VALUES
(1,3,1,560,'Completed'),
(2,4,2,820,'Completed'),
(3,3,3,420,'Completed'),
(4,9,4,750,'Completed'),
(5,4,5,620,'Completed'),
(6,3,6,980,'Completed'),
(7,9,7,340,'Completed'),
(8,4,8,1120,'Completed'),
(9,3,9,470,'Completed'),
(10,9,10,630,'Completed');

INSERT INTO OrderDetails
(OrderID, ItemID, Quantity, Subtotal)
VALUES
(1,6,1,320),
(1,10,2,120),
(1,21,2,120),

(2,15,1,450),
(2,24,2,300),
(2,17,1,180),

(3,8,1,300),
(3,28,3,120),

(4,9,1,380),
(4,20,1,220),
(4,23,1,90),

(5,14,1,350),
(5,29,2,80),

(6,6,2,640),
(6,25,2,340),

(7,3,2,240),
(7,30,1,70),

(8,15,2,900),
(8,16,1,120),

(9,12,1,220),
(9,27,2,240),

(10,13,2,480),
(10,22,1,60);

INSERT INTO Payments
(OrderID, PaymentMethod, PaymentStatus)
VALUES
(1,'UPI','Paid'),
(2,'Card','Paid'),
(3,'Cash','Paid'),
(4,'UPI','Paid'),
(5,'Card','Paid'),
(6,'Cash','Paid'),
(7,'UPI','Paid'),
(8,'Card','Paid'),
(9,'Cash','Paid'),
(10,'UPI','Paid');

SELECT * FROM Customers;
SELECT * FROM Employees;
SELECT * FROM MenuItems;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
SELECT * FROM Payments;

SELECT COUNT(*) FROM Customers;
SELECT COUNT(*) FROM Employees;
SELECT COUNT(*) FROM MenuItems;
SELECT COUNT(*) FROM Orders;
SELECT COUNT(*) FROM OrderDetails;
SELECT COUNT(*) FROM Payments;