# 🍽️ Restaurant Management System

A Restaurant Management System developed using **Python** and **MySQL** to manage customers, menu items, orders, payments, and business reports. The project also includes data analysis and visualization using **Pandas** and **Matplotlib** to provide meaningful business insights.

---
## Live url - https://restaurantmangement.streamlit.app/

## 📖 Project Overview

The Restaurant Management System is designed to simplify restaurant operations by maintaining customer records, managing menu items, processing orders, handling payments, and generating reports. It demonstrates CRUD operations, SQL concepts, and Python database connectivity.

The project also includes an analytics dashboard that visualizes restaurant data and helps understand sales trends, customer behavior, employee performance, and menu popularity.

---

## ✨ Features

### Customer Management
- Add Customer
- View Customers
- Search Customer
- Update Customer
- Delete Customer

### Menu Management
- Add Menu Item
- View Menu
- Search Menu Item
- Update Menu Item
- Delete Menu Item

### Order Management
- Place New Orders
- View Orders
- Search Orders
- Update Order Status
- Delete Orders

### Payment Management
- Record Payments
- View Payments
- Search Payments

### Reports
- Customer Order Summary
- Sales Summary
- Total Revenue
- Top Selling Items
- Top Customers
- Payment Report

---

# 🛠️ Technologies Used

### Programming Language
- Python 3.x

### Database
- MySQL for the CRUD scripts and SQL seed files
- CSV files for the analytics dashboard

### Python Libraries
- mysql-connector-python
- pandas
- matplotlib

### Tools
- MySQL Workbench
- Jupyter Notebook
- VS Code
- Git & GitHub

---

# 🗄️ Database Design

The project consists of the following tables:

- Customers
- Employees
- RestaurantTables
- Categories
- MenuItems
- Orders
- OrderDetails
- Payments

---

# 📂 Project Structure

```
Restaurant-Management-System/
│
├── SQL/
│   ├── schema.sql
│   ├── insert_data.sql
│   ├── business_queries.sql
│   ├── views.sql
│   ├── procedures.sql
│   ├── triggers.sql
│   └── indexes.sql
│
├── Python/
│   ├── db.py
│   ├── customer.py
│   ├── menu.py
│   ├── order.py
│   ├── payment.py
│   ├── reports.py
│   └── main.py
│
├── Notebook/
│   └── analysis.ipynb
│
├── data/
│   ├── Customers.csv
│   ├── Employees.csv
│   ├── MenuItems.csv
│   ├── Orders.csv
│   ├── OrderDetails.csv
│   ├── Payments.csv
│   ├── Categories.csv
│   └── RestaurantTables.csv
│
├── Screenshots/
│
├── requirements.txt
└── README.md
```

---

# 📊 Database Features

## SQL Queries
- 18+ Business Queries
- Aggregate Functions
- GROUP BY
- HAVING
- Nested Queries
- Window Functions
- Joins

## Views
- CustomerOrderSummary
- MenuCategoryView
- PaymentReport
- SalesSummary

## Stored Procedures
- GetCustomerOrders()
- GetMenuByCategory()
- GetTotalRevenue()
- GetTopSellingItems()

## Triggers
- Prevent Negative Prices
- Auto Update Table Status

## Indexes
- Customer Phone Index
- Menu Item Name Index
- Order Date Index
- Payment Status Index

---

# 📈 Data Analysis

The project includes a Jupyter Notebook (`analysis.ipynb`) for business analytics.

### Key Performance Indicators (KPIs)

- Total Revenue
- Total Orders
- Average Order Value
- Total Customers
- Total Employees

### Visualizations

- Monthly Revenue Trend
- Daily Sales Trend
- Revenue by Category
- Payment Method Distribution
- Top Selling Menu Items
- Top Customers
- Peak Ordering Hours
- Employee Performance
- Customer Spending Distribution

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/Restaurant-Management-System.git
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Export Dashboard Data

Export these tables to CSV and place them in the `data/` folder:

- Customers.csv
- Employees.csv
- MenuItems.csv
- Orders.csv
- OrderDetails.csv
- Payments.csv
- Categories.csv
- RestaurantTables.csv

The dashboard reads these files directly, so MySQL does not need to be running for analytics.

You can regenerate the CSVs from the bundled SQL seed data with:

```bash
python export_csv_data.py
```

---

## 4. Run Application

```bash
python main.py
```

---

## 5. Run Analysis Notebook

Open:

```
analysis.ipynb
```

Run all cells.

---

# 📸 Screenshots

Add screenshots of:

- Main Menu
- Customer Module
- Menu Module
- Order Module
- Payment Module
- Reports
- SQL Tables
- Sales Dashboard
- Revenue Charts
- Top Customers Analysis

---

# 📌 Future Enhancements

- User Authentication
- Inventory Management
- Online Table Reservation
- Billing & Invoice Generation
- Email Notifications
- Export Reports to Excel/PDF
- Streamlit Web Dashboard

---

# 👩‍💻 Author

**Ishita Tiwari**

B.Tech Computer Science Engineering

---

# ⭐ If you found this project useful, consider giving it a star!
