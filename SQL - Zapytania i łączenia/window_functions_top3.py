import sqlite3
import numpy as np
import pandas as pd


# ============================================================
# 1. GENEROWANIE DANYCH
# ============================================================

rng = np.random.default_rng(42)

products = [
    (1, "Elektronika", "Laptop"),
    (2, "Elektronika", "Smartfon"),
    (3, "Elektronika", "Monitor"),
    (4, "Elektronika", "Tablet"),
    (5, "Elektronika", "Sluchawki"),

    (6, "Meble", "Biurko"),
    (7, "Meble", "Krzeslo"),
    (8, "Meble", "Szafa"),
    (9, "Meble", "Stol"),
    (10, "Meble", "Regal"),

    (11, "Akcesoria", "Plecak"),
    (12, "Akcesoria", "Mysz"),
    (13, "Akcesoria", "Klawiatura"),
    (14, "Akcesoria", "Kubek"),
    (15, "Akcesoria", "Podkladka"),
]

sales_data = []
sale_id = 1

# Każdy produkt otrzymuje 20 transakcji
for product_id, category, product_name in products:

    for _ in range(20):

        revenue = round(
            float(rng.uniform(50, 2500)),
            2
        )

        sales_data.append((
            sale_id,
            product_id,
            revenue
        ))

        sale_id += 1


# ============================================================
# 2. UTWORZENIE BAZY I TABEL
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    product TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    revenue REAL NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
)
""")

conn.executemany("""
INSERT INTO products (
    product_id,
    category,
    product
)
VALUES (?, ?, ?)
""", products)

conn.executemany("""
INSERT INTO sales (
    sale_id,
    product_id,
    revenue
)
VALUES (?, ?, ?)
""", sales_data)

conn.commit()


# ============================================================
# 3. RANK() I ROW_NUMBER()
# ============================================================

query = """
WITH product_revenue AS (

    SELECT
        p.category,
        p.product,
        SUM(s.revenue) AS revenue

    FROM products p

    INNER JOIN sales s
        ON p.product_id = s.product_id

    GROUP BY
        p.category,
        p.product

),

ranked_products AS (

    SELECT
        category,
        product,
        revenue,

        RANK() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS ranking,

        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY revenue DESC, product ASC
        ) AS row_number

    FROM product_revenue
)

SELECT
    category,
    product,
    ROUND(revenue, 2) AS revenue,
    ranking,
    row_number

FROM ranked_products

WHERE row_number <= 3

ORDER BY
    category,
    row_number
"""


# ============================================================
# 4. PREZENTACJA WYNIKÓW
# ============================================================

df_top3 = pd.read_sql_query(
    query,
    conn
)

print("TOP 3 NAJLEPIEJ SPRZEDAJĄCYCH SIĘ PRODUKTÓW")
print("Ranking według przychodu w każdej kategorii:\n")

print(df_top3.to_string(index=False))


# ============================================================
# 5. PORÓWNANIE RANK() I ROW_NUMBER()
# ============================================================

print("\nWYJAŚNIENIE FUNKCJI:")
print("RANK()       - nadaje pozycję w rankingu; przy remisach")
print("               kolejne pozycje mogą zostać pominięte.")
print("ROW_NUMBER() - nadaje każdemu wierszowi unikalny numer.")
print("               Tutaj zapewnia dokładnie 3 produkty")
print("               w każdej kategorii.")


# ============================================================
# 6. WALIDACJA
# ============================================================

expected_categories = 3
expected_products_per_category = 3

category_counts = (
    df_top3.groupby("category")
    .size()
)

if len(df_top3) != expected_categories * expected_products_per_category:
    raise ValueError("Nieprawidłowa liczba produktów w TOP 3.")

if len(category_counts) != expected_categories:
    raise ValueError("Nieprawidłowa liczba kategorii.")

if not (category_counts == expected_products_per_category).all():
    raise ValueError("Każda kategoria musi zawierać dokładnie 3 produkty.")

if not (df_top3["row_number"] <= 3).all():
    raise ValueError("Wynik zawiera produkt spoza TOP 3.")

for category, group in df_top3.groupby("category"):
    revenues = group["revenue"].tolist()

    if revenues != sorted(revenues, reverse=True):
        raise ValueError(
            f"Nieprawidłowa kolejność przychodów: {category}"
        )

    if group["row_number"].tolist() != [1, 2, 3]:
        raise ValueError(
            f"Nieprawidłowa numeracja ROW_NUMBER: {category}"
        )

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Liczba kategorii: {len(category_counts)}")
print(f"Liczba produktów w TOP 3: {len(df_top3)}")

conn.close()
