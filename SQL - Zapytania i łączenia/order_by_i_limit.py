import sqlite3
import pandas as pd


# Utworzenie bazy SQLite w pamięci
conn = sqlite3.connect(":memory:")

# Dane produktów
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

# Wstawienie danych
conn.executemany("""
INSERT INTO products (product_id, name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products_data)

conn.commit()


# ZAPYTANIE 1: TOP 5 najdroższych produktów
query_expensive = """
SELECT *
FROM products
ORDER BY price DESC
LIMIT 5
"""

print("TOP 5 NAJDROŻSZYCH PRODUKTÓW:")
print(pd.read_sql_query(query_expensive, conn).to_string(index=False))


# ZAPYTANIE 2: 5 produktów z najmniejszym zapasem
query_low_stock = """
SELECT *
FROM products
ORDER BY stock ASC
LIMIT 5
"""

print("\n5 PRODUKTÓW Z NAJMNIEJSZYM ZAPASEM:")
print(pd.read_sql_query(query_low_stock, conn).to_string(index=False))


# ZAPYTANIE 3: sortowanie alfabetyczne według nazwy
query_alphabetical = """
SELECT *
FROM products
ORDER BY name ASC
"""

print("\nPRODUKTY POSORTOWANE ALFABETYCZNIE:")
print(pd.read_sql_query(query_alphabetical, conn).to_string(index=False))


conn.close()
