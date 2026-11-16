import sqlite3
import numpy as np
import pandas as pd


# ============================================================
# 1. GENEROWANIE 1000 LOSOWYCH TRANSAKCJI
# ============================================================

rng = np.random.default_rng(42)

record_count = 1000

products = [
    "Laptop",
    "Smartfon",
    "Monitor",
    "Klawiatura",
    "Mysz",
    "Sluchawki",
    "Biurko",
    "Krzeslo",
    "Plecak",
    "Kubek"
]

categories = [
    "Elektronika",
    "Meble",
    "Akcesoria"
]

product_categories = {
    "Laptop": "Elektronika",
    "Smartfon": "Elektronika",
    "Monitor": "Elektronika",
    "Klawiatura": "Elektronika",
    "Mysz": "Elektronika",
    "Sluchawki": "Elektronika",
    "Biurko": "Meble",
    "Krzeslo": "Meble",
    "Plecak": "Akcesoria",
    "Kubek": "Akcesoria"
}

# Losowanie produktów
selected_products = rng.choice(
    products,
    size=record_count
)

# Kategoria przypisana do produktu
selected_categories = [
    product_categories[product]
    for product in selected_products
]

# Losowanie dat w 2024 roku
start_date = np.datetime64("2024-01-01")
end_date = np.datetime64("2025-01-01")

random_days = rng.integers(
    0,
    int((end_date - start_date) / np.timedelta64(1, "D")),
    size=record_count
)

selected_dates = start_date + random_days.astype("timedelta64[D]")

# Losowanie przychodów
selected_revenues = rng.uniform(
    50,
    3000,
    size=record_count
).round(2)

# Przygotowanie rekordów
sales_data = [
    (
        int(i + 1),
        str(selected_products[i]),
        str(selected_categories[i]),
        str(selected_dates[i]),
        float(selected_revenues[i])
    )
    for i in range(record_count)
]


# ============================================================
# 2. UTWORZENIE BAZY I TABELI SALES
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    sale_date TEXT NOT NULL,
    revenue REAL NOT NULL
)
""")

conn.executemany("""
INSERT INTO sales (
    sale_id,
    product,
    category,
    sale_date,
    revenue
)
VALUES (?, ?, ?, ?, ?)
""", sales_data)

conn.commit()


# ============================================================
# 3. KONTROLA LICZBY REKORDÓW
# ============================================================

df_count = pd.read_sql_query(
    "SELECT COUNT(*) AS total_transactions FROM sales",
    conn
)

print("LICZBA TRANSAKCJI:")
print(df_count.to_string(index=False))


# ============================================================
# 4. ANALIZA MIESIĘCZNA
# ============================================================

query_monthly = """
SELECT
    strftime('%Y-%m', sale_date) AS month,
    SUM(revenue) AS monthly_revenue,
    COUNT(*) AS transaction_count,
    AVG(revenue) AS average_transaction
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
ORDER BY month
"""

df_monthly = pd.read_sql_query(query_monthly, conn)

print("\nPODSUMOWANIE SPRZEDAŻY MIESIĘCZNEJ:")
print(df_monthly.to_string(index=False))


# ============================================================
# 5. TEKSTOWA WIZUALIZACJA PRZYCHODÓW
# ============================================================

print("\nTEKSTOWY TREND PRZYCHODÓW:")
print("Skala: 1 znak █ = 500 PLN")

for _, row in df_monthly.iterrows():

    bar_length = int(row["monthly_revenue"] / 500)
    bar = "█" * bar_length

    print(
        f"{row['month']}: "
        f"{row['monthly_revenue']:.2f} PLN | {bar}"
    )


# ============================================================
# 6. MIESIĄCE Z PRZYCHODEM POWYŻEJ ŚREDNIEJ
# ============================================================

query_above_average = """
SELECT
    strftime('%Y-%m', sale_date) AS month,
    SUM(revenue) AS monthly_revenue,
    COUNT(*) AS transaction_count,
    AVG(revenue) AS average_transaction
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
HAVING SUM(revenue) > (
    SELECT AVG(monthly_revenue)
    FROM (
        SELECT
            SUM(revenue) AS monthly_revenue
        FROM sales
        GROUP BY strftime('%Y-%m', sale_date)
    )
)
ORDER BY monthly_revenue DESC
"""

df_above_average = pd.read_sql_query(
    query_above_average,
    conn
)

print("\nMIESIĄCE Z PRZYCHODEM POWYŻEJ ŚREDNIEJ:")
print(df_above_average.to_string(index=False))


# ============================================================
# 7. WALIDACJA
# ============================================================

if len(df_monthly) != 12:
    raise ValueError(
        f"Oczekiwano 12 miesięcy, otrzymano {len(df_monthly)}."
    )

if df_count.loc[0, "total_transactions"] != 1000:
    raise ValueError(
        "Liczba transakcji jest różna od 1000."
    )

if df_monthly["transaction_count"].sum() != 1000:
    raise ValueError(
        "Suma miesięcznych transakcji nie wynosi 1000."
    )

print("\nWALIDACJA: 1000 transakcji i 12 miesięcy.")

conn.close()
