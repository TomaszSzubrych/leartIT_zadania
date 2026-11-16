import sqlite3
import pandas as pd


# Utworzenie bazy SQLite w pamięci
conn = sqlite3.connect(":memory:")

# Dane produktów z Zadania 1
products_data = [
    (1, "Laptop", "Elektronika", 3500.00, 10),
    (2, "Mysz", "Akcesoria", 45.00, 120),
    (3, "Klawiatura", "Akcesoria", 180.00, 65),
    (4, "Monitor", "Elektronika", 1250.00, 20),
    (5, "Sluchawki", "Akcesoria", 150.00, 45),
    (6, "Smartfon", "Elektronika", 2800.00, 15),
    (7, "Drukarka", "Elektronika", 650.00, 12),
    (8, "Podkladka", "Akcesoria", 25.00, 200),
    (9, "Tablet", "Elektronika", 1600.00, 18),
    (10, "Glosniki", "Akcesoria", 220.00, 30)
]

# Utworzenie tabeli
conn.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# Wstawienie produktów
conn.executemany("""
INSERT INTO products (product_id, name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products_data)

conn.commit()


# ZAPYTANIE 1: produkty droższe niż 100 PLN
query_expensive = """
SELECT *
FROM products
WHERE price > 100
"""

print("PRODUKTY DROŻSZE NIŻ 100 PLN:")
print(pd.read_sql_query(query_expensive, conn).to_string(index=False))


# ZAPYTANIE 2: elektronika LUB cena poniżej 50 PLN
query_electronics_or_cheap = """
SELECT *
FROM products
WHERE category = 'Elektronika' OR price < 50
"""

print("\nELEKTRONIKA LUB PRODUKTY PONIŻEJ 50 PLN:")
print(pd.read_sql_query(query_electronics_or_cheap, conn).to_string(index=False))


# ZAPYTANIE 3: zapas między 10 a 50
query_stock_range = """
SELECT *
FROM products
WHERE stock BETWEEN 10 AND 50
"""

print("\nPRODUKTY Z ZAPASEM OD 10 DO 50:")
print(pd.read_sql_query(query_stock_range, conn).to_string(index=False))


conn.close()
