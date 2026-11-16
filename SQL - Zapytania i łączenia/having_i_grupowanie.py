import sqlite3
import pandas as pd


# ============================================================
# 1. POŁĄCZENIE Z BAZĄ
# ============================================================

conn = sqlite3.connect(":memory:")

# ============================================================
# 2. DANE SPRZEDAŻOWE
# ============================================================

sales_data = [
    (1, "Laptop", "Elektronika", 1200.00),
    (2, "Monitor", "Elektronika", 800.00),
    (3, "Smartfon", "Elektronika", 1500.00),
    (4, "Klawiatura", "Elektronika", 700.00),

    (5, "Biurko", "Meble", 900.00),
    (6, "Szafa", "Meble", 1100.00),
    (7, "Krzeslo", "Meble", 600.00),

    (8, "Plecak", "Akcesoria", 300.00),
    (9, "Kubek", "Akcesoria", 250.00),
    (10, "Torba", "Akcesoria", 400.00),
    (11, "Bidon", "Akcesoria", 150.00),

    (12, "Koszulka", "Odziez", 200.00),
    (13, "Bluza", "Odziez", 300.00)
]

# ============================================================
# 3. UTWORZENIE TABELI
# ============================================================

conn.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    revenue REAL NOT NULL
)
""")

# ============================================================
# 4. WSTAWIENIE DANYCH
# ============================================================

conn.executemany("""
INSERT INTO sales (sale_id, product, category, revenue)
VALUES (?, ?, ?, ?)
""", sales_data)

conn.commit()


# ============================================================
# 5. GROUP BY + HAVING
# ============================================================

query = """
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS average_revenue
FROM sales
GROUP BY category
HAVING SUM(revenue) > 1000
ORDER BY total_revenue DESC
"""

df_sales = pd.read_sql_query(query, conn)

print("ANALIZA SPRZEDAŻY — KATEGORIE Z PRZYCHODEM POWYŻEJ 1000 PLN:")
print(df_sales.to_string(index=False))


conn.close()
