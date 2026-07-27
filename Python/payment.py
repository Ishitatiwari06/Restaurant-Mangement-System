from db import get_connection


def view_payments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        P.PaymentID,
        P.OrderID,
        C.CustomerName,
        P.PaymentMethod,
        P.PaymentStatus,
        O.TotalAmount,
        P.PaymentDate
    FROM Payments P
    JOIN Orders O
    ON P.OrderID=O.OrderID
    JOIN Customers C
    ON O.CustomerID=C.CustomerID
    ORDER BY PaymentID
    """)

    rows = cursor.fetchall()

    print("\n" + "="*100)
    print("PAYMENTS")
    print("="*100)

    print("{:<5}{:<8}{:<20}{:<10}{:<12}{:<12}{}".format(
        "ID",
        "Order",
        "Customer",
        "Method",
        "Status",
        "Amount",
        "Date"
    ))

    print("-"*100)

    for row in rows:

        print("{:<5}{:<8}{:<20}{:<10}{:<12}{:<12}{}".format(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            str(row[6])
        ))

    cursor.close()
    conn.close()

def search_payment():

    conn = get_connection()
    cursor = conn.cursor()

    payment_id = int(input("\nEnter Payment ID : "))

    cursor.execute("""
    SELECT
        PaymentID,
        OrderID,
        PaymentMethod,
        PaymentStatus,
        PaymentDate
    FROM Payments
    WHERE PaymentID=%s
    """,(payment_id,))

    row = cursor.fetchone()

    if row:

        print("\nPayment Details")

        print("-"*40)

        print("Payment ID :",row[0])
        print("Order ID :",row[1])
        print("Method :",row[2])
        print("Status :",row[3])
        print("Date :",row[4])

    else:

        print("Payment Not Found")

    cursor.close()
    conn.close()

def update_payment_status():

    conn=None
    cursor=None

    try:

        conn=get_connection()
        cursor=conn.cursor()

        payment_id=int(input("\nEnter Payment ID : "))

        cursor.execute("""
        SELECT PaymentStatus
        FROM Payments
        WHERE PaymentID=%s
        """,(payment_id,))

        row=cursor.fetchone()

        if row is None:

            print("Payment Not Found")
            return

        print("\nCurrent Status :",row[0])

        print("1. Pending")
        print("2. Paid")

        choice=input("\nChoose Status : ")

        if choice=="1":
            status="Pending"

        elif choice=="2":
            status="Paid"

        else:
            print("Invalid Choice")
            return

        cursor.execute("""
        UPDATE Payments
        SET PaymentStatus=%s
        WHERE PaymentID=%s
        """,
        (
            status,
            payment_id
        ))

        conn.commit()

        print("\nPayment Updated Successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print(e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

def delete_payment():

    conn=None
    cursor=None

    try:

        conn=get_connection()
        cursor=conn.cursor()

        payment_id=int(input("\nEnter Payment ID : "))

        cursor.execute("""
        DELETE FROM Payments
        WHERE PaymentID=%s
        """,(payment_id,))

        if cursor.rowcount==0:

            print("Payment Not Found")

        else:

            conn.commit()

            print("\nPayment Deleted Successfully!")

    except Exception as e:

        if conn:
            conn.rollback()

        print(e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()