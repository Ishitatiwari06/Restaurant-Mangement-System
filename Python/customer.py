from db import get_connection


def add_customer():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        name = input("Enter Customer Name: ")
        phone = input("Enter Phone: ")
        email = input("Enter Email: ")

        query = """
        INSERT INTO Customers
        (CustomerName, Phone, Email)
        VALUES (%s,%s,%s)
        """

        cursor.execute(query, (name, phone, email))

        conn.commit()

        print("\nCustomer Added Successfully!")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def view_customers():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Customers")

        rows = cursor.fetchall()

        print("\n========== CUSTOMERS ==========\n")

        for row in rows:
            print(row)

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def search_customer():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        customer_id = int(input("Enter Customer ID: "))

        query = """
        SELECT *
        FROM Customers
        WHERE CustomerID=%s
        """

        cursor.execute(query, (customer_id,))

        row = cursor.fetchone()

        if row:
            print(row)
        else:
            print("Customer Not Found")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

from db import get_connection

def update_customer():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        customer_id = int(input("Enter Customer ID: "))

        # Check if customer exists
        cursor.execute(
            "SELECT Phone, Email FROM Customers WHERE CustomerID=%s",
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            print("Customer not found!")
            return

        current_phone, current_email = customer

        print("\nLeave blank if you don't want to change a field.")

        phone = input("New Phone : ")
        email = input("New Email : ")

        if phone == "":
            phone = current_phone

        if email == "":
            email = current_email

        query = """
        UPDATE Customers
        SET Phone=%s,
            Email=%s
        WHERE CustomerID=%s
        """

        cursor.execute(query, (phone, email, customer_id))
        conn.commit()

        print("Customer Updated Successfully!")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def delete_customer():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        customer_id = int(input("Enter Customer ID: "))

        query = """
        DELETE FROM Customers
        WHERE CustomerID=%s
        """

        cursor.execute(query, (customer_id,))

        conn.commit()

        print("Customer Deleted Successfully")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

