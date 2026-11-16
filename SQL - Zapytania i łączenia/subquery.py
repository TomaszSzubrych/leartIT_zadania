import sqlite3
import pandas as pd


# ============================================================
# 1. POŁĄCZENIE Z BAZĄ
# ============================================================

conn = sqlite3.connect(":memory:")

# ============================================================
# 2. DANE PRODUKTÓW
# ============================================================

products_data = [
    (1, "Laptop", "Elektronika", 3500.00, 12),
    (2, "Smartfon", "Elektronika", 2200.00, 20),
    (3, "Sluchawki", "Elektronika", 180.00, 35),
    (4, "Klawiatura", "Elektronika", 120.00, 40),
    (5, "Mysz", "Elektronika", 65.00, 50),
    (6, "Biurko", "Meble", 650.00, 8),
    (7, "Krzeslo", "Meble", 420.00, 15),
    (8, "Regal", "Meble", 550.00, 10),
    (9, "Kubek", "Akcesoria", 25.00, 100),
    (10, "Plecak", "Akcesoria", 140.00, 30)
]

# ============================================================
# 3. UTWORZENIE TABELI
# ============================================================

conn.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# ============================================================
# 4. WSTAWIENIE DANYCH
# ============================================================

conn.executemany("""
INSERT INTO products (product_id, name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products_data)

conn.commit()


# ============================================================
# 5. ŚREDNIA CENA WSZYSTKICH PRODUKTÓW
# ============================================================

query_average = """
SELECT AVG(price) AS average_price
FROM products
"""

df_average = pd.read_sql_query(query_average, conn)

average_price = df_average.loc[0, "average_price"]

print("ŚREDNIA CENA WSZYSTKICH PRODUKTÓW:")
print(f"{average_price:.2f}")


# ============================================================
# 6. SUBQUERY — PRODUKTY DROŻSZE OD ŚREDNIEJ
# ============================================================

query_above_average = """
SELECT
    name,
    price,
    price - (SELECT AVG(price) FROM products) AS difference,
    (
        (price - (SELECT AVG(price) FROM products))
        / (SELECT AVG(price) FROM products)
    ) * 100 AS percentage_above_average
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC
"""

df_above_average = pd.read_sql_query(
    query_above_average,
    conn
)

print("\nPRODUKTY DROŻSZE OD ŚREDNIEJ CENY:")
print(df_above_average.to_string(index=False))


# ============================================================
# 7. WALIDACJA
# ============================================================

if df_above_average.empty:
    raise ValueError(
        "Nie znaleziono produktów droższych od średniej."
    )

if not (df_above_average["price"] > average_price).all():
    raise ValueError(
        "Wynik zawiera produkt, którego cena nie przekracza średniej."
    )

print("\nWALIDACJA: wszystkie znalezione produkty są droższe od średniej.")

conn.close()
