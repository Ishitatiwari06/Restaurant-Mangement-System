from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"


def parse_value(token: str) -> str:
    token = token.strip()
    if token.upper() == "NULL":
        return ""
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1].replace("''", "'")
    return token


def parse_insert_rows(source_path: Path, table_name: str) -> tuple[list[str], list[list[str]]]:
    text = source_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"INSERT INTO\s+{re.escape(table_name)}\s*\((.*?)\)\s*VALUES\s*(.*?);",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Could not find INSERT block for {table_name} in {source_path}")

    columns = [column.strip().strip("`") for column in match.group(1).split(",")]
    values_block = match.group(2)
    row_strings = re.findall(r"\(([^()]*)\)", values_block, re.DOTALL)
    rows = []
    for row_string in row_strings:
        parts = [parse_value(part) for part in row_string.split(",")]
        rows.append(parts)
    return columns, rows


def write_csv(name: str, columns: list[str], rows: list[list[str]]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    output_path = DATA_DIR / name
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)


def main() -> None:
    schema_path = ROOT_DIR / "database" / "Schema.sql"
    transactions_path = ROOT_DIR / "transaction_data.sql"

    schema_tables = {
        "Customers": ("Customers.csv", "CustomerID"),
        "Employees": ("Employees.csv", "EmployeeID"),
        "RestaurantTables": ("RestaurantTables.csv", "TableID"),
        "Categories": ("Categories.csv", "CategoryID"),
        "MenuItems": ("MenuItems.csv", "ItemID"),
    }
    transaction_tables = {
        "Orders": "Orders.csv",
        "OrderDetails": "OrderDetails.csv",
        "Payments": "Payments.csv",
    }

    for table_name, (output_name, id_column) in schema_tables.items():
        columns, rows = parse_insert_rows(schema_path, table_name)
        rows_with_ids = [[str(index)] + row for index, row in enumerate(rows, start=1)]
        write_csv(output_name, [id_column] + columns, rows_with_ids)

    orders_columns, orders_rows = parse_insert_rows(transactions_path, "Orders")
    orders_with_ids = [[str(index)] + row for index, row in enumerate(orders_rows, start=1)]
    write_csv("Orders.csv", ["OrderID"] + orders_columns, orders_with_ids)

    details_columns, details_rows = parse_insert_rows(transactions_path, "OrderDetails")
    details_with_ids = [[str(index)] + row for index, row in enumerate(details_rows, start=1)]
    write_csv("OrderDetails.csv", ["DetailID"] + details_columns, details_with_ids)

    payments_columns, payments_rows = parse_insert_rows(transactions_path, "Payments")
    payments_with_ids = [[str(index)] + row for index, row in enumerate(payments_rows, start=1)]
    write_csv("Payments.csv", ["PaymentID"] + payments_columns, payments_with_ids)

    print(f"Exported CSV files to {DATA_DIR}")


if __name__ == "__main__":
    main()