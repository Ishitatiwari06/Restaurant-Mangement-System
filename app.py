from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent
PYTHON_DIR = ROOT_DIR / "Python"

if PYTHON_DIR.exists() and str(PYTHON_DIR) not in sys.path:
	sys.path.insert(0, str(PYTHON_DIR))

try:
	from db import get_connection
except Exception:

	def get_connection():
		return mysql.connector.connect(
			host="localhost",
			user="root",
			password="root",
			database="RestaurantDB",
		)


st.set_page_config(
	page_title="Restaurant Analytics",
	page_icon="🍽️",
	layout="wide",
)


st.markdown(
	"""
	<style>
		.block-container {
			padding-top: 1.5rem;
			padding-bottom: 2rem;
		}
	</style>
	""",
	unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, pd.DataFrame]:
	connection = get_connection()
	try:
		def read_table(query: str) -> pd.DataFrame:
			cursor = connection.cursor()
			try:
				cursor.execute(query)
				rows = cursor.fetchall()
				columns = [column[0] for column in cursor.description or []]
			finally:
				cursor.close()
			return pd.DataFrame(rows, columns=columns)

		customers = read_table("SELECT * FROM Customers")
		employees = read_table("SELECT * FROM Employees")
		menu = read_table("SELECT * FROM MenuItems")
		orders = read_table("SELECT * FROM Orders")
		order_details = read_table("SELECT * FROM OrderDetails")
		payments = read_table("SELECT * FROM Payments")
		categories = read_table("SELECT * FROM Categories")
		tables = read_table("SELECT * FROM RestaurantTables")
	finally:
		connection.close()

	orders["OrderDate"] = pd.to_datetime(orders["OrderDate"], errors="coerce")
	payments["PaymentDate"] = pd.to_datetime(payments["PaymentDate"], errors="coerce")

	return {
		"customers": customers,
		"employees": employees,
		"menu": menu,
		"orders": orders,
		"order_details": order_details,
		"payments": payments,
		"categories": categories,
		"tables": tables,
	}


def make_figure(figsize: tuple[int, int] = (8, 5)) -> plt.Figure:
	fig = plt.figure(figsize=figsize)
	return fig


def render_chart(fig: plt.Figure) -> None:
	st.pyplot(fig, clear_figure=True)


def normalize_date_range(selected_range: object, min_date, max_date):
	if isinstance(selected_range, tuple) and len(selected_range) == 2:
		return selected_range
	if isinstance(selected_range, list) and len(selected_range) == 2:
		return selected_range[0], selected_range[1]
	if selected_range is None:
		return min_date, max_date
	return selected_range, selected_range


def filter_orders(orders: pd.DataFrame, start_date, end_date, status_filter: list[str]) -> pd.DataFrame:
	if orders.empty:
		return orders.copy()

	filtered = orders.copy()
	filtered = filtered.loc[filtered["OrderDate"].notna()].copy()
	filtered = filtered.loc[
		(filtered["OrderDate"].dt.date >= start_date)
		& (filtered["OrderDate"].dt.date <= end_date)
	]

	if status_filter:
		filtered = filtered.loc[filtered["Status"].isin(status_filter)]

	return filtered


def calculate_kpis(
	filtered_orders: pd.DataFrame,
	customers: pd.DataFrame,
	employees: pd.DataFrame,
	menu: pd.DataFrame,
) -> pd.DataFrame:
	total_revenue = float(filtered_orders["TotalAmount"].sum()) if not filtered_orders.empty else 0.0
	total_orders = int(len(filtered_orders))
	total_customers = int(filtered_orders["CustomerID"].nunique()) if not filtered_orders.empty else 0
	average_order_value = round(float(filtered_orders["TotalAmount"].mean()), 2) if not filtered_orders.empty else 0.0

	return pd.DataFrame(
		{
			"Metric": [
				"Total Revenue",
				"Total Orders",
				"Total Customers",
				"Average Order Value",
				"Total Employees",
				"Total Menu Items",
			],
			"Value": [
				total_revenue,
				total_orders,
				total_customers,
				average_order_value,
				len(employees),
				len(menu),
			],
		}
	)


def show_metrics(kpi: pd.DataFrame) -> None:
	metric_map = dict(zip(kpi["Metric"], kpi["Value"], strict=False))
	columns = st.columns(3)
	columns[0].metric("Total Revenue", f"₹{metric_map['Total Revenue']:,.2f}")
	columns[1].metric("Total Orders", f"{int(metric_map['Total Orders']):,}")
	columns[2].metric("Average Order Value", f"₹{metric_map['Average Order Value']:,.2f}")

	columns = st.columns(3)
	columns[0].metric("Total Customers", f"{int(metric_map['Total Customers']):,}")
	columns[1].metric("Total Employees", f"{int(metric_map['Total Employees']):,}")
	columns[2].metric("Total Menu Items", f"{int(metric_map['Total Menu Items']):,}")


def build_dashboard(data: dict[str, pd.DataFrame]) -> None:
	customers = data["customers"]
	employees = data["employees"]
	menu = data["menu"]
	orders = data["orders"]
	order_details = data["order_details"]
	payments = data["payments"]
	categories = data["categories"]

	st.title("Restaurant Analytics Dashboard")
	st.caption("Streamlit version of the Restaurants_Analytics notebook")

	with st.sidebar:
		st.header("Filters")

		if orders.empty or orders["OrderDate"].dropna().empty:
			st.warning("No order dates available for filtering.")
			start_date = end_date = pd.Timestamp.today().date()
		else:
			min_date = orders["OrderDate"].min().date()
			max_date = orders["OrderDate"].max().date()
			selected_range = st.date_input(
				"Order date range",
				value=(min_date, max_date),
				min_value=min_date,
				max_value=max_date,
			)
			start_date, end_date = normalize_date_range(selected_range, min_date, max_date)

		status_options = sorted([value for value in orders["Status"].dropna().unique().tolist()])
		status_filter = st.multiselect(
			"Order status",
			options=status_options,
			default=status_options,
		)

		st.divider()
		st.write("Active filters")
		st.write(f"Date: {start_date} to {end_date}")
		st.write(f"Status: {', '.join(status_filter) if status_filter else 'None'}")

	filtered_orders = filter_orders(orders, start_date, end_date, status_filter)
	kpi = calculate_kpis(filtered_orders, customers, employees, menu)

	show_metrics(kpi)

	st.subheader("KPI Summary")
	st.dataframe(kpi, width="stretch", hide_index=True)

	if filtered_orders.empty:
		st.warning("No orders match the selected filters.")
		return

	filtered_orders = filtered_orders.copy()
	filtered_orders["YearMonth"] = filtered_orders["OrderDate"].dt.to_period("M").astype(str)
	filtered_orders["OrderDay"] = filtered_orders["OrderDate"].dt.date
	filtered_orders["Hour"] = filtered_orders["OrderDate"].dt.hour

	monthly_sales = filtered_orders.groupby("YearMonth", as_index=False)["TotalAmount"].sum()
	daily_sales = filtered_orders.groupby("OrderDay", as_index=False)["TotalAmount"].sum()

	payment_sales = payments.merge(filtered_orders[["OrderID", "TotalAmount"]], on="OrderID", how="inner")
	payment_summary = payment_sales.groupby("PaymentMethod", dropna=False)["TotalAmount"].sum()
	payment_summary = pd.to_numeric(payment_summary, errors="coerce").fillna(0)

	category_sales = (
		order_details.merge(filtered_orders[["OrderID"]], on="OrderID", how="inner")
		.merge(menu, on="ItemID", how="inner")
		.merge(categories, on="CategoryID", how="inner")
	)

	category_revenue = category_sales.groupby("CategoryName")["Subtotal"].sum().sort_values(ascending=False)
	top_items = category_sales.groupby("ItemName")["Quantity"].sum().sort_values(ascending=False).head(10)

	customer_sales = filtered_orders.merge(customers, on="CustomerID", how="inner")
	top_customers = customer_sales.groupby("CustomerName")["TotalAmount"].sum().sort_values(ascending=False).head(10)

	hourly_orders = filtered_orders.groupby("Hour")["OrderID"].count().reset_index(name="TotalOrders")
	status_summary = filtered_orders["Status"].value_counts()

	employee_orders = filtered_orders.merge(employees, on="EmployeeID", how="inner")
	employee_summary = employee_orders.groupby("EmployeeName")["OrderID"].count().sort_values(ascending=False)

	customer_spending = filtered_orders.groupby("CustomerID")["TotalAmount"].sum()
	average_customer_spending = customer_sales.groupby("CustomerName")["TotalAmount"].mean().sort_values(ascending=False).head(10)

	tab_sales, tab_customers, tab_operations, tab_audit = st.tabs(
		["Sales Trends", "Customer Insights", "Operations", "Data Quality"]
	)

	with tab_sales:
		left, right = st.columns(2)

		with left:
			st.subheader("Monthly Revenue Trend")
			fig = make_figure((8, 5))
			plt.plot(monthly_sales["YearMonth"], monthly_sales["TotalAmount"], marker="o", linewidth=2)
			plt.title("Monthly Revenue Trend")
			plt.xlabel("Month")
			plt.ylabel("Revenue (₹)")
			plt.grid(True)
			plt.xticks(rotation=45)
			plt.tight_layout()
			render_chart(fig)

		with right:
			st.subheader("Daily Sales Trend")
			fig = make_figure((8, 5))
			plt.plot(daily_sales["OrderDay"], daily_sales["TotalAmount"], marker="o")
			plt.title("Daily Sales Trend")
			plt.xlabel("Date")
			plt.ylabel("Revenue (₹)")
			plt.xticks(rotation=45)
			plt.tight_layout()
			render_chart(fig)

		left, right = st.columns(2)

		with left:
			st.subheader("Revenue by Payment Method")
			fig = make_figure((6, 6))
			if payment_summary.empty or float(payment_summary.sum()) == 0:
				plt.text(0.5, 0.5, "No payment data available", ha="center", va="center")
				plt.axis("off")
			else:
				plt.pie(
					payment_summary.values,
					labels=payment_summary.index.astype(str),
					autopct="%1.1f%%",
					startangle=90,
				)
				plt.title("Revenue by Payment Method")
			render_chart(fig)

		with right:
			st.subheader("Revenue by Category")
			fig = make_figure((8, 5))
			plt.bar(category_revenue.index, category_revenue.values)
			plt.title("Revenue by Category")
			plt.xlabel("Category")
			plt.ylabel("Revenue (₹)")
			plt.xticks(rotation=30, ha="right")
			plt.tight_layout()
			render_chart(fig)

	with tab_customers:
		left, right = st.columns(2)

		with left:
			st.subheader("Top 10 Selling Menu Items")
			fig = make_figure((9, 6))
			plt.barh(top_items.index, top_items.values)
			plt.title("Top 10 Selling Menu Items")
			plt.xlabel("Quantity Sold")
			plt.gca().invert_yaxis()
			plt.tight_layout()
			render_chart(fig)

		with right:
			st.subheader("Top Customers by Spending")
			fig = make_figure((10, 5))
			plt.bar(top_customers.index, top_customers.values)
			plt.title("Top Customers by Spending")
			plt.xticks(rotation=45, ha="right")
			plt.ylabel("Total Amount (₹)")
			plt.tight_layout()
			render_chart(fig)

		left, right = st.columns(2)

		with left:
			st.subheader("Customer Spending Distribution")
			fig = make_figure((8, 5))
			plt.hist(customer_spending, bins=8)
			plt.title("Customer Spending Distribution")
			plt.xlabel("Total Spending (₹)")
			plt.ylabel("Number of Customers")
			plt.tight_layout()
			render_chart(fig)

		with right:
			st.subheader("Top 10 Customers by Average Spending")
			fig = make_figure((10, 5))
			plt.bar(average_customer_spending.index, average_customer_spending.values)
			plt.xticks(rotation=45, ha="right")
			plt.title("Top 10 Customers by Average Spending")
			plt.ylabel("Average Amount (₹)")
			plt.tight_layout()
			render_chart(fig)

	with tab_operations:
		left, right = st.columns(2)

		with left:
			st.subheader("Peak Ordering Hours")
			fig = make_figure((8, 5))
			plt.bar(hourly_orders["Hour"], hourly_orders["TotalOrders"])
			plt.title("Peak Ordering Hours")
			plt.xlabel("Hour of Day")
			plt.ylabel("Number of Orders")
			plt.xticks(hourly_orders["Hour"])
			plt.tight_layout()
			render_chart(fig)

		with right:
			st.subheader("Order Status Distribution")
			fig = make_figure((6, 6))
			plt.pie(
				status_summary,
				labels=status_summary.index,
				autopct="%1.1f%%",
				startangle=90,
			)
			plt.title("Order Status Distribution")
			render_chart(fig)

		st.subheader("Orders Handled by Employees")
		fig = make_figure((10, 5))
		plt.bar(employee_summary.index, employee_summary.values)
		plt.xticks(rotation=45, ha="right")
		plt.title("Orders Handled by Employees")
		plt.ylabel("Orders")
		plt.tight_layout()
		render_chart(fig)

	with tab_audit:
		st.subheader("Preview Tables")
		table_choice = st.selectbox(
			"Select a table",
			["Customers", "Employees", "MenuItems", "Orders", "OrderDetails", "Payments", "Categories", "RestaurantTables"],
		)

		preview_map = {
			"Customers": customers,
			"Employees": employees,
			"MenuItems": menu,
			"Orders": orders,
			"OrderDetails": order_details,
			"Payments": payments,
			"Categories": categories,
			"RestaurantTables": data["tables"],
		}

		st.dataframe(preview_map[table_choice].head(), width="stretch")

		st.subheader("Missing Values")
		audit_columns = st.columns(2)
		audit_columns[0].write("Customers")
		audit_columns[0].dataframe(customers.isnull().sum(), width="stretch")
		audit_columns[1].write("Employees")
		audit_columns[1].dataframe(employees.isnull().sum(), width="stretch")

		audit_columns = st.columns(2)
		audit_columns[0].write("MenuItems")
		audit_columns[0].dataframe(menu.isnull().sum(), width="stretch")
		audit_columns[1].write("Orders")
		audit_columns[1].dataframe(orders.isnull().sum(), width="stretch")

		st.write("Duplicates")
		st.dataframe(
			pd.DataFrame(
				{
					"Table": ["Customers", "Employees", "MenuItems", "Orders", "Payments"],
					"Duplicate Rows": [
						customers.duplicated().sum(),
						employees.duplicated().sum(),
						menu.duplicated().sum(),
						orders.duplicated().sum(),
						payments.duplicated().sum(),
					],
				}
			),
			width="stretch",
			hide_index=True,
		)


def main() -> None:
	try:
		data = load_data()
	except Exception as error:
		st.title("Restaurant Analytics Dashboard")
		st.error(f"Unable to load data from MySQL: {error}")
		st.info("Check that MySQL is running and that the RestaurantDB schema has been created.")
		return

	build_dashboard(data)


if __name__ == "__main__":
	main()
