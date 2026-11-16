import sqlite3
import pandas as pd


# ============================================================
# 1. POŁĄCZENIE Z BAZĄ
# ============================================================

conn = sqlite3.connect(":memory:")

# ============================================================
# 2. DANE KLIENTÓW
# ============================================================

customers_data = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zajac", "Wroclaw"),
    (5, "Tomasz Lewandowski", "Poznan")
]

# ============================================================
# 3. DANE ZAMÓWIEŃ
# ============================================================

orders_data = [
    (101, 1, "2026-01-10"),
    (102, 2, "2026-01-11"),
    (103, 1, "2026-01-12"),
    (104, 3, "2026-01-13"),
    (105, 4, "2026-01-14"),
    (106, 2, "2026-01-15"),
    (107, 5, "2026-01-16"),
    (108, 3, "2026-01-17"),
    (109, 4, "2026-01-18"),
    (110, 5, "2026-01-19"),
    (111, 1, "2026-01-20")
]

# ============================================================
# 4. DANE POZYCJI ZAMÓWIEŃ
# order_item_id, order_id, product_name, price, quantity
# ============================================================

order_items_data = [
    (1, 101, "Laptop", 3500.00, 1),
    (2, 101, "Mysz", 65.00, 2),
    (3, 102, "Smartfon", 2200.00, 1),
    (4, 102, "Sluchawki", 180.00, 2),
    (5, 103, "Monitor", 1200.00, 2),
    (6, 103, "Klawiatura", 120.00, 1),
    (7, 104, "Biurko", 650.00, 1),
    (8, 104, "Krzeslo", 420.00, 1),
    (9, 105, "Laptop", 3500.00, 2),
    (10, 105, "Sluchawki", 180.00, 1),
    (11, 106, "Smartfon", 2200.00, 2),
    (12, 107, "Plecak", 140.00, 3),
    (13, 107, "Kubek", 25.00, 5),
    (14, 108, "Regał", 550.00, 2),
    (15, 108, "Biurko", 650.00, 1),
    (16, 109, "Monitor", 1200.00, 3),
    (17, 110, "Laptop", 3500.00, 1),
    (18, 110, "Klawiatura", 120.00, 2),
    (19, 111, "Smartfon", 2200.00, 1),
    (20, 111, "Mysz", 65.00, 3)
]

# ============================================================
# 5. TWORZENIE TABEL
# ============================================================

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
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

conn.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
""")

# ============================================================
# 6. WSTAWIANIE DANYCH
# ============================================================

conn.executemany("""
INSERT INTO customers (customer_id, name, city)
VALUES (?, ?, ?)
""", customers_data)

conn.executemany("""
INSERT INTO orders (order_id, customer_id, order_date)
VALUES (?, ?, ?)
""", orders_data)

conn.executemany("""
INSERT INTO order_items
    (order_item_id, order_id, product_name, price, quantity)
VALUES (?, ?, ?, ?, ?)
""", order_items_data)

conn.commit()


# ============================================================
# 7. JOIN TRZECH TABEL
# ============================================================

query_details = """
SELECT
    c.name AS customer_name,
    o.order_date,
    oi.product_name,
    oi.price,
    oi.quantity,
    oi.price * oi.quantity AS item_value,
    o.order_id
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
ORDER BY o.order_id, oi.order_item_id
"""

df_details = pd.read_sql_query(query_details, conn)

print("SZCZEGÓŁY ZAMÓWIEŃ — JOIN 3 TABEL:")
print(df_details.to_string(index=False))


# ============================================================
# 8. ŁĄCZNA WARTOŚĆ KAŻDEGO ZAMÓWIENIA
# ============================================================

query_order_totals = """
SELECT
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    SUM(oi.price * oi.quantity) AS order_total
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    c.name,
    o.order_date
ORDER BY order_total DESC
"""

df_order_totals = pd.read_sql_query(query_order_totals, conn)

print("\nŁĄCZNA WARTOŚĆ KAŻDEGO ZAMÓWIENIA:")
print(df_order_totals.to_string(index=False))


# ============================================================
# 9. TOP 10 NAJWIĘKSZYCH ZAMÓWIEŃ
# ============================================================

query_top_10 = query_order_totals + "\nLIMIT 10"

df_top_10 = pd.read_sql_query(query_top_10, conn)

print("\nTOP 10 NAJWIĘKSZYCH ZAMÓWIEŃ:")
print(df_top_10.to_string(index=False))


conn.close()
