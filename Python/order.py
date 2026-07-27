from db import get_connection

# ==========================================================
# PLACE ORDER
# ==========================================================

def place_order():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("PLACE ORDER")
        print("=" * 60)

        cursor.execute("""
            SELECT CustomerID, CustomerName
            FROM Customers
            ORDER BY CustomerID
        """)

        customers = cursor.fetchall()

        print("\nCustomers")
        print("-" * 40)
        print("{:<10}{}".format("ID", "Customer"))
        print("-" * 40)

        for customer in customers:
            print("{:<10}{}".format(customer[0], customer[1]))

        customer_id = int(input("\nEnter Customer ID : "))

        cursor.execute("""
            SELECT CustomerID
            FROM Customers
            WHERE CustomerID=%s
        """, (customer_id,))

        if cursor.fetchone() is None:
            print("Invalid Customer ID")
            return


        cursor.execute("""
            SELECT TableID, Capacity
            FROM RestaurantTables
            WHERE Status='Available'
            ORDER BY TableID
        """)

        tables = cursor.fetchall()

        if not tables:
            print("No Tables Available")
            return

        print("\nAvailable Tables")
        print("-" * 40)
        print("{:<10}{}".format("Table", "Capacity"))
        print("-" * 40)

        for table in tables:
            print("{:<10}{}".format(table[0], table[1]))

        table_id = int(input("\nEnter Table ID : "))

        cursor.execute("""
            SELECT TableID
            FROM RestaurantTables
            WHERE TableID=%s
            AND Status='Available'
        """, (table_id,))

        if cursor.fetchone() is None:
            print("Invalid Table")
            return


        cursor.execute("""
            SELECT EmployeeID, EmployeeName
            FROM Employees
            WHERE Role='Waiter'
            ORDER BY EmployeeID
        """)

        waiters = cursor.fetchall()

        print("\nAvailable Waiters")
        print("-" * 40)
        print("{:<10}{}".format("ID", "Waiter"))
        print("-" * 40)

        for waiter in waiters:
            print("{:<10}{}".format(waiter[0], waiter[1]))

        employee_id = int(input("\nEnter Waiter ID : "))

        cursor.execute("""
            SELECT EmployeeID
            FROM Employees
            WHERE EmployeeID=%s
            AND Role='Waiter'
        """, (employee_id,))

        if cursor.fetchone() is None:
            print("Invalid Waiter")
            return


        cursor.execute("""
            SELECT
                M.ItemID,
                M.ItemName,
                C.CategoryName,
                M.Price
            FROM MenuItems M
            JOIN Categories C
            ON M.CategoryID=C.CategoryID
            WHERE Availability='Available'
            ORDER BY ItemID
        """)

        menu = cursor.fetchall()

        print("\nRestaurant Menu")
        print("-" * 90)
        print("{:<5}{:<30}{:<20}{:<10}".format(
            "ID",
            "Item",
            "Category",
            "Price"
        ))
        print("-" * 90)

        for item in menu:

            print("{:<5}{:<30}{:<20}{:<10}".format(
                item[0],
                item[1],
                item[2],
                item[3]
            ))


        order_items = []

        while True:

            item_id = int(input("\nEnter Item ID : "))
            quantity = int(input("Enter Quantity : "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue

            cursor.execute("""
                SELECT ItemName, Price
                FROM MenuItems
                WHERE ItemID=%s
                AND Availability='Available'
            """, (item_id,))

            result = cursor.fetchone()

            if result is None:
                print("Invalid Item ID")
                continue

            item_name = result[0]
            price = float(result[1])

            duplicate = False

            for i in range(len(order_items)):

                if order_items[i][0] == item_id:

                    new_qty = order_items[i][3] + quantity
                    new_subtotal = new_qty * price

                    order_items[i] = (
                        item_id,
                        item_name,
                        price,
                        new_qty,
                        new_subtotal
                    )

                    duplicate = True
                    break

            if not duplicate:

                subtotal = price * quantity

                order_items.append(
                    (
                        item_id,
                        item_name,
                        price,
                        quantity,
                        subtotal
                    )
                )

            choice = input("\nAdd another item? (Y/N): ").upper()

            if choice == "N":
                break

        total_amount = sum(item[4] for item in order_items)

        print("\n")
        print("=" * 60)
        print("ORDER SUMMARY")
        print("=" * 60)

        print("{:<30}{:<10}{:<10}{:<10}".format(
            "Item",
            "Price",
            "Qty",
            "Subtotal"
        ))

        print("-" * 60)

        for item in order_items:

            print("{:<30}{:<10}{:<10}{:<10}".format(
                item[1],
                item[2],
                item[3],
                item[4]
            ))

        print("-" * 60)
        print("Total Bill :", total_amount)


        cursor.execute("""
            INSERT INTO Orders
            (
                CustomerID,
                EmployeeID,
                TableID,
                TotalAmount,
                Status
            )
            VALUES
            (%s,%s,%s,%s,'Completed')
        """,
        (
            customer_id,
            employee_id,
            table_id,
            total_amount
        ))

        order_id = cursor.lastrowid


        for item in order_items:

            cursor.execute("""
                INSERT INTO OrderDetails
                (
                    OrderID,
                    ItemID,
                    Quantity,
                    Subtotal
                )
                VALUES
                (%s,%s,%s,%s)
            """,
            (
                order_id,
                item[0],
                item[3],
                item[4]
            ))


        cursor.execute("""
            UPDATE RestaurantTables
            SET Status='Occupied'
            WHERE TableID=%s
        """, (table_id,))

        conn.commit()

        print("\n" + "=" * 50)
        print("ORDER PLACED SUCCESSFULLY")
        print("=" * 50)
        print("Order ID :", order_id)
        print("Total Bill :", total_amount)

    except Exception as e:

        if conn:
            conn.rollback()

        print("\nTransaction Failed")
        print(e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================================
# VIEW ORDERS
# ==========================================================

def view_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            O.OrderID,
            C.CustomerName,
            E.EmployeeName,
            O.OrderDate,
            O.TotalAmount,
            O.Status
        FROM Orders O
        JOIN Customers C
        ON O.CustomerID=C.CustomerID
        JOIN Employees E
        ON O.EmployeeID=E.EmployeeID
        ORDER BY O.OrderID
    """)

    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print("ALL ORDERS")
    print("=" * 90)

    print("{:<8}{:<20}{:<18}{:<22}{:<12}{}".format(
        "ID",
        "Customer",
        "Waiter",
        "Date",
        "Amount",
        "Status"
    ))

    print("-" * 90)

    for row in rows:

        print("{:<8}{:<20}{:<18}{:<22}{:<12}{}".format(
            row[0],
            row[1],
            row[2],
            str(row[3]),
            row[4],
            row[5]
        ))

    cursor.close()
    conn.close()


# ==========================================================
# SEARCH ORDER
# ==========================================================

def search_order():

    conn = get_connection()
    cursor = conn.cursor()

    order_id = int(input("\nEnter Order ID : "))

    cursor.execute("""
        SELECT
            O.OrderID,
            C.CustomerName,
            E.EmployeeName,
            O.OrderDate,
            O.TotalAmount,
            O.Status
        FROM Orders O
        JOIN Customers C
        ON O.CustomerID=C.CustomerID
        JOIN Employees E
        ON O.EmployeeID=E.EmployeeID
        WHERE O.OrderID=%s
    """, (order_id,))

    row = cursor.fetchone()

    if row is None:

        print("Order Not Found")

    else:

        print("\nOrder Details")
        print("-" * 40)
        print("Order ID :", row[0])
        print("Customer :", row[1])
        print("Waiter   :", row[2])
        print("Date     :", row[3])
        print("Amount   :", row[4])
        print("Status   :", row[5])

    cursor.close()
    conn.close()

# ==========================================================
# UPDATE ORDER STATUS
# ==========================================================

def update_order_status():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        order_id = int(input("\nEnter Order ID : "))

        cursor.execute("""
            SELECT Status
            FROM Orders
            WHERE OrderID=%s
        """, (order_id,))

        result = cursor.fetchone()

        if result is None:
            print("Order Not Found")
            return

        print("\nCurrent Status :", result[0])

        print("\n1. Pending")
        print("2. Completed")

        choice = input("\nEnter New Status : ")

        if choice == "1":
            status = "Pending"

        elif choice == "2":
            status = "Completed"

        else:
            print("Invalid Choice")
            return

        cursor.execute("""
            UPDATE Orders
            SET Status=%s
            WHERE OrderID=%s
        """,
        (
            status,
            order_id
        ))

        conn.commit()

        print("\nOrder Status Updated Successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print(e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ==========================================================
# DELETE ORDER
# ==========================================================

def delete_order():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        order_id = int(input("\nEnter Order ID : "))

        cursor.execute("""
            SELECT TableID
            FROM Orders
            WHERE OrderID=%s
        """, (order_id,))

        result = cursor.fetchone()

        if result is None:
            print("Order Not Found")
            return

        table_id = result[0]

        confirm = input(
            "\nDelete this order? (Y/N): "
        ).upper()

        if confirm != "Y":
            print("Deletion Cancelled")
            return

        # Delete Payment

        cursor.execute("""
            DELETE FROM Payments
            WHERE OrderID=%s
        """, (order_id,))

        # Delete Order Details

        cursor.execute("""
            DELETE FROM OrderDetails
            WHERE OrderID=%s
        """, (order_id,))

        # Delete Order

        cursor.execute("""
            DELETE FROM Orders
            WHERE OrderID=%s
        """, (order_id,))

        # Free Table

        cursor.execute("""
            UPDATE RestaurantTables
            SET Status='Available'
            WHERE TableID=%s
        """,
        (table_id,))

        conn.commit()

        print("\nOrder Deleted Successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print(e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()