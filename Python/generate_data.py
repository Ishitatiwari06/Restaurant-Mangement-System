import random

random.seed(42)

# -------------------------
# Menu Prices
# -------------------------

prices = {
    1:180,2:250,3:120,4:220,5:150,
    6:320,7:280,8:300,9:380,10:60,
    11:180,12:220,13:240,14:350,15:450,
    16:120,17:180,18:100,19:140,20:220,
    21:60,22:60,23:90,24:150,25:170,
    26:80,27:120,28:40,29:40,30:70
}

payment_methods = ["Cash", "Card", "UPI"]

orders_sql = []
details_sql = []
payments_sql = []

detail_id = 1

for order_id in range(1, 41):

    customer = random.randint(1, 20)

    employee = random.choice([3, 4, 9])      # waiters

    table = random.randint(1, 10)

    month = random.randint(1, 6)
    day = random.randint(1, 28)

    hour = random.randint(12, 21)

    minute = random.randint(0, 59)

    order_date = f"2026-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:00"

    items = random.randint(2, 4)

    chosen = random.sample(list(prices.keys()), items)

    total = 0

    for item in chosen:

        qty = random.randint(1, 3)

        subtotal = qty * prices[item]

        total += subtotal

        details_sql.append(
            f"({order_id},{item},{qty},{subtotal})"
        )

    orders_sql.append(
        f"({customer},{employee},{table},'{order_date}',{total},'Completed')"
    )

    method = random.choice(payment_methods)

    payments_sql.append(
        f"({order_id},'{method}','Paid','{order_date}')"
    )

# -------------------------
# Save SQL
# -------------------------

with open("transaction_data.sql", "w") as f:

    f.write("INSERT INTO Orders\n")
    f.write("(CustomerID,EmployeeID,TableID,OrderDate,TotalAmount,Status)\nVALUES\n")
    f.write(",\n".join(orders_sql))
    f.write(";\n\n")

    f.write("INSERT INTO OrderDetails\n")
    f.write("(OrderID,ItemID,Quantity,Subtotal)\nVALUES\n")
    f.write(",\n".join(details_sql))
    f.write(";\n\n")

    f.write("INSERT INTO Payments\n")
    f.write("(OrderID,PaymentMethod,PaymentStatus,PaymentDate)\nVALUES\n")
    f.write(",\n".join(payments_sql))
    f.write(";\n")

print("transaction_data.sql generated successfully!")