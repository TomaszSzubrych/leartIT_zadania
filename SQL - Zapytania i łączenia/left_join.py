import sqlite3
import pandas as pd


conn = sqlite3.connect(":memory:")

# Dane klientów — Karolina nie ma zamówienia
customers_data = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zajac", "Wroclaw"),
    (5, "Tomasz Lewandowski", "Poznan"),
    (6, "Karolina Nowicka", "Lodz")
]

# Dane zamówień
orders_data = [
    (101, 1, 250.00),
    (102, 2, 120.50),
    (103, 1, 340.00),
    (104, 3, 80.00),
    (105, 4, 450.00),
    (106, 2, 175.00),
    (107, 5, 520.00),
    (108, 3, 95.00)
]

# Utworzenie tabel
conn.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL
)
""")

# Wstawienie danych
conn.executemany("""
INSERT INTO customers (customer_id, name, city)
VALUES (?, ?, ?)
""", customers_data)

conn.executemany("""
INSERT INTO orders (order_id, customer_id, amount)
VALUES (?, ?, ?)
""", orders_data)

conn.commit()


# ZAPYTANIE 1: LEFT JOIN — wszyscy klienci
query_all_customers = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    COALESCE(o.amount, 0) AS amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id
"""

print("WSZYSCY KLIENCI — LEFT JOIN:")
print(pd.read_sql_query(query_all_customers, conn).to_string(index=False))


# ZAPYTANIE 2: klienci bez zamówień
query_without_orders = """
SELECT
    c.customer_id,
    c.name,
    c.city
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
"""

print("\nKLIENCI BEZ ZAMÓWIEŃ:")
print(pd.read_sql_query(query_without_orders, conn).to_string(index=False))


conn.close()
