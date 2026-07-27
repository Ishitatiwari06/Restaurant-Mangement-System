from customer import *
from menu import *
from order import *
from payment import *

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

def order_menu():

    while True:

        print("\n" + "=" * 50)
        print("          ORDER MANAGEMENT")
        print("=" * 50)

        print("1. Place Order")
        print("2. View Orders")
        print("3. Search Order")
        print("4. Update Order Status")
        print("5. Delete Order")
        print("6. Back")

        choice = input("\nEnter your choice : ")

        if choice == "1":
            place_order()

        elif choice == "2":
            view_orders()

        elif choice == "3":
            search_order()

        elif choice == "4":
            update_order_status()

        elif choice == "5":
            delete_order()

        elif choice == "6":
            break

        else:
            print("Invalid Choice!")

def payment_menu():

    while True:

        print("\n" + "=" * 50)
        print("         PAYMENT MANAGEMENT")
        print("=" * 50)

        print("1. View Payments")
        print("2. Search Payment")
        print("3. Update Payment Status")
        print("4. Delete Payment")
        print("5. Back")

        choice = input("\nEnter your choice : ")

        if choice == "1":
            view_payments()

        elif choice == "2":
            search_payment()

        elif choice == "3":
            update_payment_status()

        elif choice == "4":
            delete_payment()

        elif choice == "5":
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
            order_menu()

        elif choice == "4":
            payment_menu()

        elif choice == "5":
            print("Reports Module Coming Soon...")

        elif choice == "6":
            print("\nThank you for using Restaurant Management System!")
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()