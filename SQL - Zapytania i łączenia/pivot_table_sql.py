import sqlite3

import numpy as np
import pandas as pd


# ============================================================
# 1. GENEROWANIE DANYCH SPRZEDAŻOWYCH
# ============================================================

rng = np.random.default_rng(42)

NUMBER_OF_SALES = 1200

date_offsets = rng.integers(
    0,
    366,
    size=NUMBER_OF_SALES
)

dates = (
    np.datetime64("2024-01-01")
    + date_offsets.astype("timedelta64[D]")
)

categories = rng.choice(
    ["A", "B"],
    size=NUMBER_OF_SALES
)

revenues = np.round(
    rng.uniform(50, 2000, size=NUMBER_OF_SALES),
    2
)

sales = [
    (
        i + 1,
        str(dates[i]),
        str(categories[i]),
        float(revenues[i])
    )
    for i in range(NUMBER_OF_SALES)
]


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    revenue REAL NOT NULL
)
""")

conn.executemany("""
INSERT INTO sales (
    sale_id,
    date,
    category,
    revenue
)
VALUES (?, ?, ?, ?)
""", sales)

conn.commit()


# ============================================================
# 3. PIVOT TABLE — CASE WHEN + GROUP BY
# ============================================================

query_pivot = """
SELECT
    strftime('%Y-%m', date) AS month,

    SUM(
        CASE
            WHEN category = 'A'
            THEN revenue
            ELSE 0
        END
    ) AS cat_A,

    SUM(
        CASE
            WHEN category = 'B'
            THEN revenue
            ELSE 0
        END
    ) AS cat_B

FROM sales

GROUP BY strftime('%Y-%m', date)

ORDER BY month
"""

df_pivot = pd.read_sql_query(
    query_pivot,
    conn
)

df_pivot[["cat_A", "cat_B"]] = (
    df_pivot[["cat_A", "cat_B"]].round(2)
)

print("PIVOT TABLE — MIESIĘCZNY PRZYCHÓD WEDŁUG KATEGORII:")
print(df_pivot.to_string(index=False))


# ============================================================
# 4. DODATKOWE PODSUMOWANIE PRZYCHODÓW
# ============================================================

df_pivot["total_revenue"] = (
    df_pivot["cat_A"] + df_pivot["cat_B"]
).round(2)

print("\nŁĄCZNY PRZYCHÓD W KAŻDYM MIESIĄCU:")
print(
    df_pivot[
        ["month", "total_revenue"]
    ].to_string(index=False)
)


# ============================================================
# 5. TEKSTOWA PREZENTACJA — DWA SŁUPKI NA MIESIĄC
# ============================================================

SCALE = 5000

print("\nTEKSTOWE SŁUPKI PRZYCHODÓW:")
print(f"Skala: 1 znak █ = {SCALE} jednostek przychodu")
print("Każdy miesiąc zawiera osobny słupek dla kategorii A i B.")

for _, row in df_pivot.iterrows():

    bar_a = "█" * int(
        row["cat_A"] / SCALE
    )

    bar_b = "█" * int(
        row["cat_B"] / SCALE
    )

    print(f"\nMIESIĄC: {row['month']}")

    print(
        f"Kategoria A: {row['cat_A']:>12.2f} | {bar_a}"
    )

    print(
        f"Kategoria B: {row['cat_B']:>12.2f} | {bar_b}"
    )


# ============================================================
# 6. WALIDACJA
# ============================================================

actual_sales_count = conn.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

actual_months = len(df_pivot)

if actual_sales_count != NUMBER_OF_SALES:
    raise ValueError("Nieprawidłowa liczba transakcji.")

if actual_months != 12:
    raise ValueError(
        f"Oczekiwano 12 miesięcy, otrzymano {actual_months}."
    )

if df_pivot[["cat_A", "cat_B"]].isna().any().any():
    raise ValueError("W pivot table występują brakujące wartości.")

if (df_pivot[["cat_A", "cat_B"]] < 0).any().any():
    raise ValueError("Wykryto ujemny przychód.")

sql_total_revenue = conn.execute(
    "SELECT SUM(revenue) FROM sales"
).fetchone()[0]

pivot_total_revenue = df_pivot[
    ["cat_A", "cat_B"]
].to_numpy().sum()

if not np.isclose(
    sql_total_revenue,
    pivot_total_revenue,
    rtol=1e-9
):
    raise ValueError(
        "Suma przychodów w pivot nie zgadza się z tabelą sales."
    )

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Liczba transakcji: {actual_sales_count}")
print(f"Liczba miesięcy: {actual_months}")
print(f"Suma przychodów SQL: {sql_total_revenue:.2f}")
print(f"Suma przychodów pivot: {pivot_total_revenue:.2f}")

conn.close()
