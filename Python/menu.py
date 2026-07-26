from db import get_connection

def add_menu_item():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 50)
        print("ADD MENU ITEM")
        print("=" * 50)

        item_name = input("Enter Item Name: ").strip()

        # Display Categories
        cursor.execute("""
            SELECT CategoryID, CategoryName
            FROM Categories
            ORDER BY CategoryID
        """)

        categories = cursor.fetchall()

        print("\nAvailable Categories")

        for category in categories:
            print(f"{category[0]}. {category[1]}")

        category_id = int(input("\nEnter Category ID: "))

        category_ids = [row[0] for row in categories]

        if category_id not in category_ids:
            print("Invalid Category!")
            return

        price = float(input("Enter Price: "))

        if price <= 0:
            print("Price must be greater than zero.")
            return

        print("\nAvailability")
        print("1. Available")
        print("2. Not Available")

        choice = input("Enter Choice: ")

        if choice == "1":
            availability = "Available"

        elif choice == "2":
            availability = "Not Available"

        else:
            print("Invalid Choice!")
            return

        query = """
        INSERT INTO MenuItems
        (ItemName, CategoryID, Price, Availability)
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (item_name, category_id, price, availability)
        )

        conn.commit()

        print("\nMenu Item Added Successfully!")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def view_menu():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            M.ItemID,
            M.ItemName,
            C.CategoryName,
            M.Price,
            M.Availability
        FROM MenuItems M
        JOIN Categories C
        ON M.CategoryID = C.CategoryID
        ORDER BY M.ItemID
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        print("\n" + "=" * 85)
        print("{:<5} {:<25} {:<18} {:<10} {:<15}".format(
            "ID",
            "Item Name",
            "Category",
            "Price",
            "Availability"
        ))
        print("=" * 85)

        for row in rows:

            print("{:<5} {:<25} {:<18} {:<10} {:<15}".format(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ))

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def search_menu_item():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        item_id = int(input("Enter Item ID: "))

        query = """
        SELECT
            M.ItemID,
            M.ItemName,
            C.CategoryName,
            M.Price,
            M.Availability
        FROM MenuItems M
        JOIN Categories C
        ON M.CategoryID = C.CategoryID
        WHERE M.ItemID=%s
        """

        cursor.execute(query, (item_id,))

        row = cursor.fetchone()

        if row:

            print("\nItem Details")
            print("-" * 30)
            print("ID          :", row[0])
            print("Name        :", row[1])
            print("Category    :", row[2])
            print("Price       :", row[3])
            print("Availability:", row[4])

        else:
            print("Menu Item Not Found")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def update_menu_item():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        item_id = int(input("Enter Item ID: "))

        cursor.execute("""
            SELECT
                ItemName,
                CategoryID,
                Price,
                Availability
            FROM MenuItems
            WHERE ItemID=%s
        """, (item_id,))

        item = cursor.fetchone()

        if item is None:
            print("Menu Item Not Found")
            return

        current_name, current_category, current_price, current_availability = item

        print("\nLeave blank to keep existing value.\n")

        name = input(f"Item Name ({current_name}): ").strip()

        if name == "":
            name = current_name

        cursor.execute("""
            SELECT CategoryID, CategoryName
            FROM Categories
        """)

        categories = cursor.fetchall()

        print("\nCategories")

        for c in categories:
            print(f"{c[0]}. {c[1]}")

        category = input(f"Category ({current_category}): ")

        if category == "":
            category = current_category
        else:
            category = int(category)

        price = input(f"Price ({current_price}): ")

        if price == "":
            price = current_price
        else:
            price = float(price)

            if price <= 0:
                print("Invalid Price")
                return

        print("\nAvailability")
        print("1. Available")
        print("2. Not Available")
        print("Press Enter to Keep Same")

        choice = input("Choice: ")

        if choice == "":
            availability = current_availability

        elif choice == "1":
            availability = "Available"

        elif choice == "2":
            availability = "Not Available"

        else:
            print("Invalid Choice")
            return

        query = """
        UPDATE MenuItems
        SET
            ItemName=%s,
            CategoryID=%s,
            Price=%s,
            Availability=%s
        WHERE ItemID=%s
        """

        cursor.execute(
            query,
            (
                name,
                category,
                price,
                availability,
                item_id
            )
        )

        conn.commit()

        print("\nMenu Updated Successfully!")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def delete_menu_item():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        item_id = int(input("Enter Item ID: "))

        cursor.execute("""
            SELECT COUNT(*)
            FROM OrderDetails
            WHERE ItemID=%s
        """, (item_id,))

        count = cursor.fetchone()[0]

        if count > 0:

            print("\nCannot Delete!")
            print("This item has already been used in orders.")
            return

        cursor.execute("""
            DELETE FROM MenuItems
            WHERE ItemID=%s
        """, (item_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Menu Item Deleted Successfully!")
        else:
            print("Menu Item Not Found")

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()