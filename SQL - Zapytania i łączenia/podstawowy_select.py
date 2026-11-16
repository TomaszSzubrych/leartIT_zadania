import sqlite3
import pandas as pd


# Utworzenie bazy SQLite w pamięci
conn = sqlite3.connect(":memory:")

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

# Przykładowe produkty
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

# Wstawienie danych do tabeli
conn.executemany("""
INSERT INTO products (product_id, name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products_data)

conn.commit()


# ZAPYTANIE 1: wszystkie produkty
query_all = """
SELECT *
FROM products
"""

all_products = pd.read_sql_query(query_all, conn)

print("WSZYSTKIE PRODUKTY:")
print(all_products.to_string(index=False))


# ZAPYTANIE 2: tylko nazwa i cena
query_name_price = """
SELECT name, price
FROM products
"""

selected_products = pd.read_sql_query(query_name_price, conn)

print("\nNAZWA I CENA PRODUKTU:")
print(selected_products.to_string(index=False))


# Zamknięcie połączenia z bazą
conn.close()
