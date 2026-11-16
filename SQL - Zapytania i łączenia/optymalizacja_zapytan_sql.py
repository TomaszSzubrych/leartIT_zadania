import sqlite3
import time

import numpy as np
import pandas as pd


# ============================================================
# 1. GENEROWANIE DANYCH — NUMPY
# ============================================================

rng = np.random.default_rng(42)

NUMBER_OF_CUSTOMERS = 10_000
NUMBER_OF_PRODUCTS = 500
NUMBER_OF_SALES = 100_000

regions = np.array([
    "North",
    "South",
    "East",
    "West"
])

categories = np.array([
    "Elektronika",
    "Meble",
    "Akcesoria",
    "Odziez",
    "Sport"
])

customers = [
    (i + 1, str(rng.choice(regions)))
    for i in range(NUMBER_OF_CUSTOMERS)
]

products = [
    (
        i + 1,
        str(categories[i % len(categories)])
    )
    for i in range(NUMBER_OF_PRODUCTS)
]

customer_ids = rng.integers(
    1,
    NUMBER_OF_CUSTOMERS + 1,
    size=NUMBER_OF_SALES
)

product_ids = rng.integers(
    1,
    NUMBER_OF_PRODUCTS + 1,
    size=NUMBER_OF_SALES
)

quantities = rng.integers(
    1,
    11,
    size=NUMBER_OF_SALES
)

unit_prices = np.round(
    rng.uniform(20, 2000, size=NUMBER_OF_SALES),
    2
)

date_offsets = rng.integers(
    0,
    366,
    size=NUMBER_OF_SALES
)

sale_dates = (
    np.datetime64("2024-01-01")
    + date_offsets.astype("timedelta64[D]")
)

sales = [
    (
        i + 1,
        int(customer_ids[i]),
        int(product_ids[i]),
        int(quantities[i]),
        float(unit_prices[i]),
        str(sale_dates[i])
    )
    for i in range(NUMBER_OF_SALES)
]

print("DANE WYGENEROWANE:")
print(f"Klienci: {len(customers):,}")
print(f"Produkty: {len(products):,}")
print(f"Transakcje: {len(sales):,}")


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    region TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    sale_date TEXT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
)
""")

conn.executemany("""
INSERT INTO customers (customer_id, region)
VALUES (?, ?)
""", customers)

conn.executemany("""
INSERT INTO products (product_id, category)
VALUES (?, ?)
""", products)

conn.executemany("""
INSERT INTO sales (
    sale_id,
    customer_id,
    product_id,
    quantity,
    unit_price,
    sale_date
)
VALUES (?, ?, ?, ?, ?, ?)
""", sales)

conn.commit()


# ============================================================
# 3. ZŁOŻONE ZAPYTANIE SQL
# ============================================================

query = """
SELECT
    p.category,
    c.region,
    COUNT(s.sale_id) AS transaction_count,
    SUM(s.quantity * s.unit_price) AS total_revenue,
    AVG(s.quantity * s.unit_price) AS average_sale

FROM sales s

INNER JOIN customers c
    ON s.customer_id = c.customer_id

INNER JOIN products p
    ON s.product_id = p.product_id

WHERE
    s.sale_date >= '2024-07-01'
    AND c.region = 'North'

GROUP BY
    p.category,
    c.region

HAVING
    SUM(s.quantity * s.unit_price) > 100000

ORDER BY
    total_revenue DESC
"""


# ============================================================
# 4. FUNKCJA POMIARU CZASU
# ============================================================

def measure_query():
    durations = []

    for _ in range(3):
        start = time.perf_counter()

        result = pd.read_sql_query(
            query,
            conn
        )

        end = time.perf_counter()

        durations.append(end - start)

    average_time = sum(durations) / len(durations)

    return average_time, result


# ============================================================
# 5. FUNKCJA ANALIZY PLANU WYKONANIA
# ============================================================

def get_query_plan():
    plan = conn.execute(
        "EXPLAIN QUERY PLAN " + query
    ).fetchall()

    return [
        str(row[3])
        for row in plan
    ]


# ============================================================
# 6. POMIAR BEZ INDEKSÓW
# ============================================================

print("\n" + "=" * 70)
print("POMIAR BAZOWY — BEZ INDEKSÓW")
print("=" * 70)

baseline_time, baseline_result = measure_query()
baseline_plan = get_query_plan()

print(f"Średni czas: {baseline_time:.6f} s")

print("\nPLAN WYKONANIA:")
for step in baseline_plan:
    print(step)

print("\nWYNIK ZAPYTANIA:")
print(baseline_result.to_string(index=False))


# ============================================================
# 7. DODAWANIE INDEKSÓW POJEDYNCZO
# ============================================================

indexes = [
    (
        "idx_customers_region",
        "CREATE INDEX idx_customers_region "
        "ON customers(region)"
    ),
    (
        "idx_sales_customer_id",
        "CREATE INDEX idx_sales_customer_id "
        "ON sales(customer_id)"
    ),
    (
        "idx_sales_product_id",
        "CREATE INDEX idx_sales_product_id "
        "ON sales(product_id)"
    ),
    (
        "idx_sales_sale_date",
        "CREATE INDEX idx_sales_sale_date "
        "ON sales(sale_date)"
    ),
    (
        "idx_products_category",
        "CREATE INDEX idx_products_category "
        "ON products(category)"
    )
]

timing_rows = [
    {
        "index": "BRAK INDEKSÓW",
        "average_time_s": baseline_time,
        "speedup": 1.0
    }
]

plan_rows = [
    {
        "stage": "BRAK INDEKSÓW",
        "plan": " | ".join(baseline_plan)
    }
]

report_rows = []

previous_plan = baseline_plan

for index_name, create_index_sql in indexes:

    print("\n" + "=" * 70)
    print(f"DODAWANIE INDEKSU: {index_name}")
    print("=" * 70)

    conn.execute(create_index_sql)
    conn.commit()

    # Aktualizacja statystyk optymalizatora
    conn.execute("ANALYZE")

    current_time, current_result = measure_query()
    current_plan = get_query_plan()

    speedup = (
        baseline_time / current_time
        if current_time > 0
        else 0
    )

    plan_changed = current_plan != previous_plan

    timing_rows.append({
        "index": index_name,
        "average_time_s": current_time,
        "speedup": speedup
    })

    plan_rows.append({
        "stage": index_name,
        "plan": " | ".join(current_plan)
    })

    report_rows.append({
        "index": index_name,
        "average_time_s": current_time,
        "speedup": speedup,
        "plan_changed": plan_changed,
        "plan": " | ".join(current_plan)
    })

    print(f"Średni czas: {current_time:.6f} s")
    print(f"Przyspieszenie względem bazy: {speedup:.2f}x")
    print(f"Zmiana planu: {'TAK' if plan_changed else 'NIE'}")

    print("\nPLAN WYKONANIA:")
    for step in current_plan:
        print(step)

    previous_plan = current_plan


# ============================================================
# 8. DATAFRAME — CZASY I PRZYSPIESZENIE
# ============================================================

df_times = pd.DataFrame(timing_rows)

print("\n" + "=" * 70)
print("DATAFRAME — CZASY WYKONANIA")
print("=" * 70)

print(
    df_times.to_string(
        index=False,
        formatters={
            "average_time_s": lambda x: f"{x:.6f}",
            "speedup": lambda x: f"{x:.2f}x"
        }
    )
)


# ============================================================
# 9. DATAFRAME — PLANY WYKONANIA
# ============================================================

df_plans = pd.DataFrame(plan_rows)

print("\n" + "=" * 70)
print("DATAFRAME — WSZYSTKIE PLANY WYKONANIA")
print("=" * 70)

for _, row in df_plans.iterrows():
    print(f"\nETAP: {row['stage']}")
    print(row["plan"])


# ============================================================
# 10. RAPORT WPŁYWU KAŻDEGO INDEKSU
# ============================================================

df_report = pd.DataFrame(report_rows)

print("\n" + "=" * 70)
print("RAPORT WPŁYWU INDEKSÓW")
print("=" * 70)

print(
    df_report[
        [
            "index",
            "average_time_s",
            "speedup",
            "plan_changed"
        ]
    ].to_string(
        index=False,
        formatters={
            "average_time_s": lambda x: f"{x:.6f}",
            "speedup": lambda x: f"{x:.2f}x"
        }
    )
)


# ============================================================
# 11. TEKSTOWE SŁUPKI PRZYSPIESZENIA
# ============================================================

print("\n" + "=" * 70)
print("TEKSTOWE SŁUPKI PRZYSPIESZENIA")
print("Skala: 1 znak █ = 1x")
print("=" * 70)

for _, row in df_times.iterrows():

    speedup = row["speedup"]

    bar_length = max(
        1,
        int(round(speedup))
    )

    bar = "█" * bar_length

    print(
        f"{row['index']:<30} "
        f"{speedup:>7.2f}x | {bar}"
    )


# ============================================================
# 12. NAJWIĘKSZY EFEKT
# ============================================================

best_index = df_report.loc[
    df_report["average_time_s"].idxmin()
]

print("\n" + "=" * 70)
print("NAJWIĘKSZY EFEKT OPTYMALIZACJI")
print("=" * 70)

print(f"Indeks: {best_index['index']}")
print(f"Czas: {best_index['average_time_s']:.6f} s")
print(f"Przyspieszenie względem bazy: {best_index['speedup']:.2f}x")
print(
    "Zmiana planu: "
    + ("TAK" if best_index["plan_changed"] else "NIE")
)


# ============================================================
# 13. WALIDACJA
# ============================================================

actual_sales_count = conn.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

actual_customers_count = conn.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

actual_products_count = conn.execute(
    "SELECT COUNT(*) FROM products"
).fetchone()[0]

if actual_sales_count != NUMBER_OF_SALES:
    raise ValueError("Nieprawidłowa liczba rekordów w tabeli sales.")

if actual_customers_count != NUMBER_OF_CUSTOMERS:
    raise ValueError("Nieprawidłowa liczba klientów.")

if actual_products_count != NUMBER_OF_PRODUCTS:
    raise ValueError("Nieprawidłowa liczba produktów.")

if len(timing_rows) != len(indexes) + 1:
    raise ValueError("Brakuje pomiarów czasu.")

if len(plan_rows) != len(indexes) + 1:
    raise ValueError("Brakuje planów wykonania.")

if len(df_report) != len(indexes):
    raise ValueError("Nieprawidłowa liczba raportowanych indeksów.")

if baseline_time <= 0:
    raise ValueError("Nieprawidłowy bazowy czas wykonania.")

if not all(
    np.isfinite(row["average_time_s"])
    and row["average_time_s"] > 0
    for row in timing_rows
):
    raise ValueError("Wykryto nieprawidłowy pomiar czasu.")

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Transakcje: {actual_sales_count:,}")
print(f"Klienci: {actual_customers_count:,}")
print(f"Produkty: {actual_products_count:,}")
print(f"Pomiarów: {len(timing_rows)}")
print(f"Planów wykonania: {len(plan_rows)}")
print(f"Utworzonych indeksów: {len(indexes)}")

conn.close()
