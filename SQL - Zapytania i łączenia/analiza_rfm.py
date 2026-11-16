import sqlite3

import numpy as np
import pandas as pd


# ============================================================
# 1. PARAMETRY I GENEROWANIE DANYCH
# ============================================================

rng = np.random.default_rng(42)

REFERENCE_DATE = "2025-01-01"
NUMBER_OF_CUSTOMERS = 200

customers = []
orders = []

order_id = 1

# Celowo tworzymy klientów z różnymi zachowaniami zakupowymi,
# aby wszystkie cztery segmenty były reprezentowane.

for customer_id in range(1, NUMBER_OF_CUSTOMERS + 1):

    if customer_id <= 50:
        # VIP: niedawne zakupy, wysoka częstotliwość
        recency_days = int(rng.integers(1, 25))
        number_of_orders = int(rng.integers(6, 13))
        amount_range = (500, 1800)

    elif customer_id <= 100:
        # Regular: umiarkowanie niedawne zakupy
        recency_days = int(rng.integers(25, 60))
        number_of_orders = int(rng.integers(3, 7))
        amount_range = (200, 1200)

    elif customer_id <= 150:
        # At-risk: dłuższy czas od ostatniego zakupu
        recency_days = int(rng.integers(61, 120))
        number_of_orders = int(rng.integers(2, 5))
        amount_range = (100, 900)

    else:
        # Lost: dawno bez zakupów
        recency_days = int(rng.integers(121, 301))
        number_of_orders = int(rng.integers(1, 4))
        amount_range = (50, 600)

    customers.append((
        customer_id,
        f"Klient_{customer_id:03d}"
    ))

    # Data ostatniego zamówienia
    last_order_date = (
        np.datetime64(REFERENCE_DATE)
        - np.timedelta64(recency_days, "D")
    )

    # Pozostałe zamówienia są starsze
    for order_number in range(number_of_orders):

        if order_number == 0:
            order_date = last_order_date
        else:
            older_days = int(
                rng.integers(1, 181)
            )

            order_date = (
                last_order_date
                - np.timedelta64(older_days, "D")
            )

        amount = round(
            float(rng.uniform(*amount_range)),
            2
        )

        orders.append((
            order_id,
            customer_id,
            str(order_date),
            amount
        ))

        order_id += 1


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
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
    name
)
VALUES (?, ?)
""", customers)

conn.executemany("""
INSERT INTO orders (
    order_id,
    customer_id,
    order_date,
    amount
)
VALUES (?, ?, ?, ?)
""", orders)

conn.commit()


# ============================================================
# 3. OBLICZENIE RFM I SEGMENTACJA
# ============================================================

query_rfm = f"""
WITH customer_rfm AS (

    SELECT
        c.customer_id,
        c.name,

        CAST(
            julianday('{REFERENCE_DATE}')
            - julianday(MAX(o.order_date))
            AS INTEGER
        ) AS recency,

        COUNT(o.order_id) AS frequency,

        COALESCE(SUM(o.amount), 0) AS monetary

    FROM customers c

    LEFT JOIN orders o
        ON c.customer_id = o.customer_id

    GROUP BY
        c.customer_id,
        c.name
),

segmented_customers AS (

    SELECT
        customer_id,
        name,
        recency,
        frequency,
        monetary,

        CASE
            WHEN recency <= 30 AND frequency >= 5
                THEN 'VIP'

            WHEN recency <= 60 AND frequency >= 3
                THEN 'Regular'

            WHEN recency <= 120
                THEN 'At-risk'

            ELSE 'Lost'
        END AS segment

    FROM customer_rfm
)

SELECT
    customer_id,
    name,
    recency,
    frequency,
    ROUND(monetary, 2) AS monetary,
    segment

FROM segmented_customers

ORDER BY
    CASE segment
        WHEN 'VIP' THEN 1
        WHEN 'Regular' THEN 2
        WHEN 'At-risk' THEN 3
        WHEN 'Lost' THEN 4
    END,
    recency
"""

df_rfm = pd.read_sql_query(
    query_rfm,
    conn
)


# ============================================================
# 4. PREZENTACJA WSKAŹNIKÓW RFM
# ============================================================

print("ANALIZA RFM — KLIENCI")
print(f"Data odniesienia: {REFERENCE_DATE}")
print("\nPrzykładowe rekordy:")

print(
    df_rfm.head(15).to_string(index=False)
)


# ============================================================
# 5. PODSUMOWANIE SEGMENTÓW
# ============================================================

query_segments = f"""
WITH customer_rfm AS (

    SELECT
        c.customer_id,

        CAST(
            julianday('{REFERENCE_DATE}')
            - julianday(MAX(o.order_date))
            AS INTEGER
        ) AS recency,

        COUNT(o.order_id) AS frequency,

        COALESCE(SUM(o.amount), 0) AS monetary

    FROM customers c

    LEFT JOIN orders o
        ON c.customer_id = o.customer_id

    GROUP BY c.customer_id
),

segmented_customers AS (

    SELECT
        customer_id,
        recency,
        frequency,
        monetary,

        CASE
            WHEN recency <= 30 AND frequency >= 5
                THEN 'VIP'

            WHEN recency <= 60 AND frequency >= 3
                THEN 'Regular'

            WHEN recency <= 120
                THEN 'At-risk'

            ELSE 'Lost'
        END AS segment

    FROM customer_rfm
)

SELECT
    segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(recency), 2) AS average_recency,
    ROUND(AVG(frequency), 2) AS average_frequency,
    ROUND(AVG(monetary), 2) AS average_monetary

FROM segmented_customers

GROUP BY segment

ORDER BY
    CASE segment
        WHEN 'VIP' THEN 1
        WHEN 'Regular' THEN 2
        WHEN 'At-risk' THEN 3
        WHEN 'Lost' THEN 4
    END
"""

df_segments = pd.read_sql_query(
    query_segments,
    conn
)

print("\nPODSUMOWANIE SEGMENTÓW RFM:")
print(df_segments.to_string(index=False))


# ============================================================
# 6. TEKSTOWE SŁUPKI LICZBY KLIENTÓW
# ============================================================

SCALE = 10

print("\nTEKSTOWE SŁUPKI LICZBY KLIENTÓW:")
print(f"Skala: 1 znak █ = {SCALE} klientów")

for _, row in df_segments.iterrows():

    customer_count = int(row["customer_count"])

    bar_length = int(
        round(customer_count / SCALE)
    )

    bar = "█" * bar_length

    print(
        f"{row['segment']:<10} "
        f"{customer_count:>3} klientów | {bar}"
    )


# ============================================================
# 7. WALIDACJA
# ============================================================

actual_customers = conn.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

actual_orders = conn.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

expected_segments = {
    "VIP",
    "Regular",
    "At-risk",
    "Lost"
}

actual_segments = set(df_rfm["segment"].unique())

if actual_customers != NUMBER_OF_CUSTOMERS:
    raise ValueError("Nieprawidłowa liczba klientów.")

if actual_orders != len(orders):
    raise ValueError("Nieprawidłowa liczba zamówień.")

if len(df_rfm) != NUMBER_OF_CUSTOMERS:
    raise ValueError("Nie każdy klient ma wynik RFM.")

if actual_segments != expected_segments:
    raise ValueError(
        f"Nieprawidłowe segmenty: {actual_segments}"
    )

if df_segments["customer_count"].sum() != NUMBER_OF_CUSTOMERS:
    raise ValueError("Liczba klientów w segmentach jest nieprawidłowa.")

if df_rfm[["recency", "frequency", "monetary"]].isna().any().any():
    raise ValueError("Wskaźniki RFM zawierają brakujące wartości.")

if (df_rfm["recency"] < 0).any():
    raise ValueError("Wykryto ujemną wartość Recency.")

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Liczba klientów: {actual_customers}")
print(f"Liczba zamówień: {actual_orders}")
print(f"Liczba segmentów: {len(df_segments)}")

conn.close()
