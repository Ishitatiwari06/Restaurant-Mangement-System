from customer import *
from menu import *

def customer_menu():

    while True:

        print("\n" + "=" * 50)
        print("        CUSTOMER MANAGEMENT")
        print("=" * 50)

        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_customer()

        elif choice == "2":
            view_customers()

        elif choice == "3":
            search_customer()

        elif choice == "4":
            update_customer()

        elif choice == "5":
            delete_customer()

        elif choice == "6":
            break

        else:
            print("Invalid Choice!")

def menu_menu():

    while True:

        print("\n" + "=" * 50)
        print("          MENU MANAGEMENT")
        print("=" * 50)

        print("1. Add Menu Item")
        print("2. View Menu")
        print("3. Search Menu Item")
        print("4. Update Menu Item")
        print("5. Delete Menu Item")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_menu_item()

        elif choice == "2":
            view_menu()

        elif choice == "3":
            search_menu_item()

        elif choice == "4":
            update_menu_item()

        elif choice == "5":
            delete_menu_item()

        elif choice == "6":
            break

        else:
            print("Invalid Choice!")


def main():

    while True:

        print("\n" + "=" * 60)
        print("      RESTAURANT MANAGEMENT SYSTEM")
        print("=" * 60)

        print("1. Customer Management")
        print("2. Menu Management")
        print("3. Order Management")
        print("4. Payment Management")
        print("5. Reports")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            customer_menu()

        elif choice == "2":
            menu_menu()

        elif choice == "3":
            print("Order Module Coming Soon...")

        elif choice == "4":
            print("Payment Module Coming Soon...")

        elif choice == "5":
            print("Reports Module Coming Soon...")

        elif choice == "6":
            print("\nThank you for using Restaurant Management System!")
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()