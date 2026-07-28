from db import get_connection

def customer_order_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM CustomerOrderSummary
    """)

    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print("CUSTOMER ORDER SUMMARY")
    print("=" * 90)

    print("{:<8}{:<20}{:<22}{:<12}{}".format(
        "Order",
        "Customer",
        "Order Date",
        "Amount",
        "Status"
    ))

    print("-" * 90)

    for row in rows:

        print("{:<8}{:<20}{:<22}{:<12}{}".format(
            row[0],
            row[1],
            str(row[2]),
            row[3],
            row[4]
        ))

    cursor.close()
    conn.close()

def menu_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM MenuCategoryView
    """)

    rows = cursor.fetchall()

    print("\n" + "=" * 90)
    print("MENU REPORT")
    print("=" * 90)

    print("{:<25}{:<18}{:<10}{}".format(
        "Item",
        "Category",
        "Price",
        "Availability"
    ))

    print("-" * 90)

    for row in rows:

        print("{:<25}{:<18}{:<10}{}".format(
            row[0],
            row[1],
            row[2],
            row[3]
        ))

    cursor.close()
    conn.close()

def payment_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM PaymentReport
    """)

    rows = cursor.fetchall()

    print("\n" + "=" * 100)
    print("PAYMENT REPORT")
    print("=" * 100)

    print("{:<6}{:<20}{:<10}{:<12}{}".format(
        "ID",
        "Customer",
        "Method",
        "Status",
        "Date"
    ))

    print("-" * 100)

    for row in rows:

        print("{:<6}{:<20}{:<10}{:<12}{}".format(
            row[0],
            row[1],
            row[2],
            row[3],
            str(row[4])
        ))

    cursor.close()
    conn.close()

def top_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        C.CustomerID,
        C.CustomerName,
        SUM(O.TotalAmount) AS TotalSpent

    FROM Customers C

    JOIN Orders O
    ON C.CustomerID = O.CustomerID

    GROUP BY
        C.CustomerID,
        C.CustomerName

    ORDER BY TotalSpent DESC

    LIMIT 5

    """)

    rows = cursor.fetchall()

    print("\nTOP 5 CUSTOMERS\n")

    print("{:<8}{:<20}{}".format(
        "ID",
        "Customer",
        "Total Spent"
    ))

    print("-" * 50)

    for row in rows:

        print("{:<8}{:<20}{}".format(
            row[0],
            row[1],
            row[2]
        ))

    cursor.close()
    conn.close()

def total_revenue():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.callproc("GetTotalRevenue")

    for result in cursor.stored_results():
        row = result.fetchone()

    print(f"Total Revenue : ₹{row[0]}")

    cursor.close()
    conn.close()

def sales_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM SalesSummary
        ORDER BY SalesDate
    """)

    rows = cursor.fetchall()

    print("\n" + "=" * 65)
    print("                SALES SUMMARY")
    print("=" * 65)

    print("{:<15}{:<15}{}".format(
        "Date",
        "Orders",
        "Revenue"
    ))

    print("-" * 65)

    for row in rows:

        print("{:<15}{:<15}₹{}".format(
            str(row[0]),
            row[1],
            row[2]
        ))

    cursor.close()
    conn.close()

def top_selling_items():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Call Stored Procedure
        cursor.callproc("GetTopSellingItems")

        print("\n" + "=" * 55)
        print("            TOP 5 SELLING ITEMS")
        print("=" * 55)

        print("{:<5}{:<30}{}".format(
            "No.",
            "Item Name",
            "Quantity Sold"
        ))

        print("-" * 55)

        for result in cursor.stored_results():

            rows = result.fetchall()

            for i, row in enumerate(rows, start=1):

                print("{:<5}{:<30}{}".format(
                    i,
                    row[0],
                    row[1]
                ))

    except Exception as e:

        print("Error :", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()