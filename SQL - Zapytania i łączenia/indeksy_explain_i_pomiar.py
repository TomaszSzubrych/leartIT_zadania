import sqlite3
import time
import numpy as np
import pandas as pd


# ============================================================
# 1. PRZYGOTOWANIE DANYCH — 10 000 REKORDÓW
# ============================================================

rng = np.random.default_rng(42)

record_count = 10_000

# Losowe wartości filtrowanej kolumny
lookup_values = rng.integers(0, 1000, size=record_count)

# Zapewniamy występowanie wartości 777
lookup_values[::100] = 777

# Dodatkowe dane liczbowe
amounts = rng.uniform(10, 1000, size=record_count).round(2)

data = [
    (int(i + 1), int(lookup_values[i]), float(amounts[i]))
    for i in range(record_count)
]


# ============================================================
# 2. UTWORZENIE BAZY I TABELI
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE records (
    record_id INTEGER PRIMARY KEY,
    lookup_value INTEGER NOT NULL,
    amount REAL NOT NULL
)
""")

conn.executemany("""
INSERT INTO records (record_id, lookup_value, amount)
VALUES (?, ?, ?)
""", data)

conn.commit()

print("LICZBA REKORDÓW W TABELI:")
print(pd.read_sql_query(
    "SELECT COUNT(*) AS total_records FROM records",
    conn
).to_string(index=False))


# ============================================================
# 3. ZAPYTANIE BEZ INDEKSU
# ============================================================

target_value = 777

query = """
SELECT record_id, lookup_value, amount
FROM records
WHERE lookup_value = ?
"""


# Pomiar czasu — średnia z 5 powtórzeń
times_without_index = []

for _ in range(5):
    start = time.perf_counter()

    result = conn.execute(query, (target_value,)).fetchall()

    end = time.perf_counter()

    times_without_index.append(end - start)

average_without_index = sum(times_without_index) / len(times_without_index)


# Plan wykonania bez indeksu
plan_without_index = pd.read_sql_query(
    """
    EXPLAIN QUERY PLAN
    SELECT record_id, lookup_value, amount
    FROM records
    WHERE lookup_value = 777
    """,
    conn
)

print("\nPLAN ZAPYTANIA BEZ INDEKSU:")
print(plan_without_index.to_string(index=False))

print("\nCZAS BEZ INDEKSU:")
print(f"Średnia z 5 pomiarów: {average_without_index:.8f} s")


# ============================================================
# 4. UTWORZENIE INDEKSU
# ============================================================

conn.execute("""
CREATE INDEX idx_records_lookup_value
ON records(lookup_value)
""")

conn.commit()


# ============================================================
# 5. ZAPYTANIE Z INDEKSEM
# ============================================================

times_with_index = []

for _ in range(5):
    start = time.perf_counter()

    result = conn.execute(query, (target_value,)).fetchall()

    end = time.perf_counter()

    times_with_index.append(end - start)

average_with_index = sum(times_with_index) / len(times_with_index)


# Plan wykonania z indeksem
plan_with_index = pd.read_sql_query(
    """
    EXPLAIN QUERY PLAN
    SELECT record_id, lookup_value, amount
    FROM records
    WHERE lookup_value = 777
    """,
    conn
)

print("\nPLAN ZAPYTANIA Z INDEKSEM:")
print(plan_with_index.to_string(index=False))

print("\nCZAS Z INDEKSEM:")
print(f"Średnia z 5 pomiarów: {average_with_index:.8f} s")


# ============================================================
# 6. PORÓWNANIE WYNIKÓW
# ============================================================

if average_with_index > 0:
    speedup = average_without_index / average_with_index
else:
    speedup = float("inf")

comparison = pd.DataFrame({
    "Wariant": ["Bez indeksu", "Z indeksem"],
    "Sredni czas (s)": [
        average_without_index,
        average_with_index
    ]
})

print("\nPORÓWNANIE CZASÓW:")
print(comparison.to_string(index=False))

print("\nPRZYSPIESZENIE:")
print(f"{speedup:.2f}x")

print("\nPODSUMOWANIE PLANÓW:")
print("Bez indeksu — oczekiwany SCAN.")
print("Z indeksem — oczekiwany SEARCH USING INDEX.")

conn.close()
