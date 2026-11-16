import sqlite3
import numpy as np
import pandas as pd


# ============================================================
# 1. GENEROWANIE DANYCH KLIENTÓW I ZAMÓWIEŃ
# ============================================================

rng = np.random.default_rng(42)

customers_data = []
orders_data = []

customer_id = 1
order_id = 1

# Sześć kohort: styczeń–czerwiec 2024
for month in range(1, 7):

    # 12 klientów w każdej kohorcie
    for _ in range(12):

        registration_start = np.datetime64(
            f"2024-{month:02d}-01"
        )

        next_month = (
            pd.Timestamp(year=2024, month=month, day=1)
            + pd.DateOffset(months=1)
        )

        registration_days = (
            next_month.to_datetime64() - registration_start
        ) / np.timedelta64(1, "D")

        registration_offset = rng.integers(
            0,
            int(registration_days)
        )

        registration_date = (
            registration_start
            + np.timedelta64(int(registration_offset), "D")
        )

        customers_data.append((
            customer_id,
            f"Klient_{customer_id:03d}",
            str(registration_date)
        ))

        # Każdy klient otrzymuje od 1 do 5 zamówień
        number_of_orders = int(rng.integers(1, 6))

        days_available = (
            np.datetime64("2025-01-01") - registration_date
        ) / np.timedelta64(1, "D")

        for _ in range(number_of_orders):

            order_offset = rng.integers(
                0,
                int(days_available)
            )

            order_date = (
                registration_date
                + np.timedelta64(int(order_offset), "D")
            )

            amount = round(
                float(rng.uniform(50, 1500)),
                2
            )

            orders_data.append((
                order_id,
                customer_id,
                str(order_date),
                amount
            ))

            order_id += 1

        customer_id += 1


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    registration_date TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")

conn.executemany("""
INSERT INTO customers (
    customer_id,
    name,
    registration_date
)
VALUES (?, ?, ?)
""", customers_data)

conn.executemany("""
INSERT INTO orders (
    order_id,
    customer_id,
    order_date,
    amount
)
VALUES (?, ?, ?, ?)
""", orders_data)

conn.commit()


# ============================================================
# 3. PODSUMOWANIE KOHORT
# ============================================================

query_cohorts = """
SELECT
    strftime('%Y-%m', c.registration_date) AS cohort,

    COUNT(DISTINCT c.customer_id) AS customer_count,

    COUNT(o.order_id) AS order_count,

    COALESCE(SUM(o.amount), 0) AS total_revenue,

    CASE
        WHEN COUNT(DISTINCT c.customer_id) > 0
        THEN COALESCE(SUM(o.amount), 0)
             / COUNT(DISTINCT c.customer_id)
        ELSE 0
    END AS ltv_per_customer

FROM customers c

LEFT JOIN orders o
    ON c.customer_id = o.customer_id

GROUP BY strftime('%Y-%m', c.registration_date)

ORDER BY cohort
"""

df_cohorts = pd.read_sql_query(
    query_cohorts,
    conn
)

print("PODSUMOWANIE KOHORT:")
print(df_cohorts.to_string(index=False))


# ============================================================
# 4. DANE DO ANALIZY KOHORTOWEJ
# ============================================================

query_cohort_months = """
SELECT
    strftime('%Y-%m', c.registration_date) AS cohort,

    (
        (CAST(strftime('%Y', o.order_date) AS INTEGER)
         - CAST(strftime('%Y', c.registration_date) AS INTEGER))
        * 12
        +
        (CAST(strftime('%m', o.order_date) AS INTEGER)
         - CAST(strftime('%m', c.registration_date) AS INTEGER))
    ) AS months_since_registration,

    SUM(o.amount) * 1.0
        / COUNT(DISTINCT c.customer_id)
        AS revenue_per_customer

FROM customers c

INNER JOIN orders o
    ON c.customer_id = o.customer_id

GROUP BY
    cohort,
    months_since_registration

ORDER BY
    cohort,
    months_since_registration
"""

df_cohort_months = pd.read_sql_query(
    query_cohort_months,
    conn
)


# ============================================================
# 5. PIVOT — KOHORTA × MIESIĄCE OD REJESTRACJI
# ============================================================

df_pivot = df_cohort_months.pivot(
    index="cohort",
    columns="months_since_registration",
    values="revenue_per_customer"
)

df_pivot.columns.name = "miesiąc_od_rejestracji"

print("\nTABELA PIVOT — PRZYCHÓD NA KLIENTA:")
print(df_pivot.round(2).to_string())


# ============================================================
# 6. KWARTYLE I TEKSTOWA HEATMAPA
# ============================================================

values = df_pivot.to_numpy().flatten()

valid_values = values[~np.isnan(values)]

q1 = np.quantile(valid_values, 0.25)
q2 = np.quantile(valid_values, 0.50)
q3 = np.quantile(valid_values, 0.75)


def value_to_symbol(value):
    if pd.isna(value):
        return "."

    if value <= q1:
        return "░"

    if value <= q2:
        return "▒"

    if value <= q3:
        return "▓"

    return "█"


df_heatmap = df_pivot.map(value_to_symbol)

print("\nTEKSTOWA HEATMAPA KOHORT:")
print(df_heatmap.to_string())


# ============================================================
# 7. LEGENDA I GRANICE KWARTYLI
# ============================================================

print("\nLEGENDA HEATMAPY:")
print(". — brak danych")
print(f"░ — niski przychód na klienta (do {q1:.2f})")
print(f"▒ — średni przychód na klienta (do {q2:.2f})")
print(f"▓ — wysoki przychód na klienta (do {q3:.2f})")
print("█ — bardzo wysoki przychód na klienta")

print("\nGRANICE KWARTYLI:")
print(f"Q1: {q1:.2f}")
print(f"Q2: {q2:.2f}")
print(f"Q3: {q3:.2f}")


# ============================================================
# 8. WALIDACJA
# ============================================================

total_customers = len(customers_data)
total_orders = len(orders_data)

if total_customers != 72:
    raise ValueError("Oczekiwano 72 klientów.")

if total_orders <= 0:
    raise ValueError("Nie wygenerowano zamówień.")

if len(df_cohorts) != 6:
    raise ValueError("Oczekiwano 6 kohort.")

if df_cohorts["customer_count"].sum() != total_customers:
    raise ValueError("Liczba klientów w kohortach jest nieprawidłowa.")

if df_cohorts["order_count"].sum() != total_orders:
    raise ValueError("Liczba zamówień w kohortach jest nieprawidłowa.")

if df_heatmap.empty:
    raise ValueError("Heatmapa jest pusta.")

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Liczba klientów: {total_customers}")
print(f"Liczba zamówień: {total_orders}")
print(f"Liczba kohort: {len(df_cohorts)}")

conn.close()
