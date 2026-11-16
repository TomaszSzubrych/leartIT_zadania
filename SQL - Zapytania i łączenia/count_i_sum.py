import sqlite3
import pandas as pd


# Połączenie z bazą SQLite w pamięci
conn = sqlite3.connect(":memory:")

# Dane produktów
products_data = [
    (1, "Laptop", "Elektronika", 3500.00, 12),
    (2, "Smartfon", "Elektronika", 2200.00, 20),
    (3, "Sluchawki", "Elektronika", 180.00, 35),
    (4, "Klawiatura", "Elektronika", 120.00, 40),
    (5, "Mysz", "Elektronika", 65.00, 50),
    (6, "Biurko", "Meble", 650.00, 8),
    (7, "Krzeslo", "Meble", 420.00, 15),
    (8, "Regał", "Meble", 550.00, 10),
    (9, "Kubek", "Akcesoria", 25.00, 100),
    (10, "Plecak", "Akcesoria", 140.00, 30)
]

# Utworzenie tabeli products
conn.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# Wstawienie danych
conn.executemany("""
INSERT INTO products (product_id, name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products_data)

conn.commit()


# 1. Łączna liczba produktów
query_count = """
SELECT
    COUNT(*) AS total_products
FROM products
"""

df_count = pd.read_sql_query(query_count, conn)

print("1. ŁĄCZNA LICZBA PRODUKTÓW:")
print(df_count.to_string(index=False))


# 2. Łączna wartość zapasów
# Wartość zapasu produktu = cena * liczba sztuk
query_stock_value = """
SELECT
    SUM(stock * price) AS total_stock_value
FROM products
"""

df_stock_value = pd.read_sql_query(query_stock_value, conn)

print("\n2. ŁĄCZNA WARTOŚĆ ZAPASÓW:")
print(df_stock_value.to_string(index=False))


# 3. Średnia cena produktów w każdej kategorii
query_average_price = """
SELECT
    category,
    AVG(price) AS average_price
FROM products
GROUP BY category
ORDER BY category
"""

df_average_price = pd.read_sql_query(query_average_price, conn)

print("\n3. ŚREDNIA CENA PRODUKTÓW W KAŻDEJ KATEGORII:")
print(df_average_price.to_string(index=False))


conn.close()
