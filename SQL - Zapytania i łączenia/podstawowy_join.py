import sqlite3
import pandas as pd


# Utworzenie bazy SQLite w pamięci
conn = sqlite3.connect(":memory:")

# Tabela klientów
customers_data = [
    (1, "Jan Kowalski", "Warszawa"),
    (2, "Anna Nowak", "Krakow"),
    (3, "Piotr Wisniewski", "Gdansk"),
    (4, "Maria Zajac", "Wroclaw"),
    (5, "Tomasz Lewandowski", "Poznan")
]

# Tabela zamówień
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

# Utworzenie tabeli customers
conn.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
""")

# Utworzenie tabeli orders
conn.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL
)
""")

# Wstawienie danych klientów
conn.executemany("""
INSERT INTO customers (customer_id, name, city)
VALUES (?, ?, ?)
""", customers_data)

# Wstawienie danych zamówień
conn.executemany("""
INSERT INTO orders (order_id, customer_id, amount)
VALUES (?, ?, ?)
""", orders_data)

conn.commit()


# INNER JOIN: klienci i ich zamówienia
query = """
SELECT
    c.name,
    c.city,
    o.amount
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC
"""

result = pd.read_sql_query(query, conn)

print("KLIENCI I ICH ZAMÓWIENIA — INNER JOIN:")
print(result.to_string(index=False))


conn.close()
