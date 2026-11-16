import sqlite3
import pandas as pd


# Połączenie z bazą SQLite w pamięci
conn = sqlite3.connect(":memory:")

# Dane zamówień — zgodne z poprzednimi zadaniami
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

# Utworzenie tabeli
conn.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL
)
""")

# Wstawienie danych
conn.executemany("""
INSERT INTO orders (order_id, customer_id, amount)
VALUES (?, ?, ?)
""", orders_data)

conn.commit()


# 1. Liczba zamówień dla każdego klienta
query_count = """
SELECT
    customer_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_count = pd.read_sql_query(query_count, conn)

print("1. LICZBA ZAMÓWIEŃ DLA KAŻDEGO KLIENTA:")
print(df_count.to_string(index=False))


# 2. Łączna kwota zamówień dla każdego klienta
query_sum = """
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_sum = pd.read_sql_query(query_sum, conn)

print("\n2. ŁĄCZNA KWOTA ZAMÓWIEŃ DLA KAŻDEGO KLIENTA:")
print(df_sum.to_string(index=False))


# 3. Średnia wartość zamówienia dla każdego klienta
query_avg = """
SELECT
    customer_id,
    AVG(amount) AS average_amount
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""

df_avg = pd.read_sql_query(query_avg, conn)

print("\n3. ŚREDNIA WARTOŚĆ ZAMÓWIENIA DLA KAŻDEGO KLIENTA:")
print(df_avg.to_string(index=False))


conn.close()
