import sqlite3
import pandas as pd
import numpy as np

from green_sql_common import (
    build_database,
    validate_database
)

from green_sql_01_nieoptymalny import run as run_nonoptimized
from green_sql_02_czesciowo_optymalny import run as run_partial
from green_sql_03_wpelni_optymalny import run as run_optimized


# ============================================================
# 1. WARIANT 1 — BEZ INDEKSÓW
# ============================================================

print("=" * 75)
print("WARIANT 1 — NIEOPTYMALNY")
print("=" * 75)

conn1 = build_database()
validate_database(conn1)

result1 = run_nonoptimized(conn1)

print("Plan wykonania:")
for step in result1["plan"]:
    print(step)

conn1.close()


# ============================================================
# 2. WARIANT 2 — INDEKSY, AGREGACJA W PYTHONIE
# ============================================================

print("\n" + "=" * 75)
print("WARIANT 2 — CZĘŚCIOWO OPTYMALNY")
print("=" * 75)

conn2 = build_database()
validate_database(conn2)

result2 = run_partial(conn2)

print("Plan wykonania:")
for step in result2["plan"]:
    print(step)

conn2.close()


# ============================================================
# 3. WARIANT 3 — PEŁNA OPTYMALIZACJA SQL
# ============================================================

print("\n" + "=" * 75)
print("WARIANT 3 — W PEŁNI OPTYMALNY")
print("=" * 75)

conn3 = build_database()
validate_database(conn3)

result3 = run_optimized(conn3)

print("Plan wykonania:")
for step in result3["plan"]:
    print(step)

conn3.close()


# ============================================================
# 4. RAPORT PORÓWNAWCZY
# ============================================================

results = [
    result1,
    result2,
    result3
]

df_report = pd.DataFrame([
    {
        "strategy": result["name"],
        "average_time_s": result["average_time"],
        "memory_bytes": result["memory_bytes"],
        "memory_KB": result["memory_bytes"] / 1024,
        "rows_fetched": result["rows_fetched"]
    }
    for result in results
])

print("\n" + "=" * 75)
print("TABELA PORÓWNAWCZA — 3 STRATEGIE")
print("=" * 75)

print(
    df_report.to_string(
        index=False,
        formatters={
            "average_time_s": lambda x: f"{x:.6f}",
            "memory_bytes": lambda x: f"{x:,}",
            "memory_KB": lambda x: f"{x:,.2f}"
        }
    )
)


# ============================================================
# 5. SŁUPKI CZASU I PAMIĘCI
# ============================================================

print("\nSŁUPKI CZASU:")
print("Skala: 1 znak █ = 10 ms")

for _, row in df_report.iterrows():
    milliseconds = row["average_time_s"] * 1000
    length = max(1, int(round(milliseconds / 10)))

    print(
        f"{row['strategy']:<25} "
        f"{milliseconds:>10.2f} ms | "
        f"{'█' * length}"
    )


print("\nSŁUPKI PAMIĘCI:")
print("Skala: 1 znak █ = 500 KB")

for _, row in df_report.iterrows():
    memory_kb = row["memory_KB"]
    length = max(1, int(round(memory_kb / 500)))

    print(
        f"{row['strategy']:<25} "
        f"{memory_kb:>12.2f} KB | "
        f"{'█' * length}"
    )


# ============================================================
# 6. PROXY ZUŻYCIA ENERGII
# ============================================================

df_report["energy_proxy"] = (
    df_report["average_time_s"]
    * df_report["memory_bytes"]
)

baseline = df_report.iloc[0]
optimized = df_report.iloc[2]

time_saving = (
    1 - optimized["average_time_s"]
    / baseline["average_time_s"]
) * 100

memory_saving = (
    1 - optimized["memory_bytes"]
    / baseline["memory_bytes"]
) * 100

energy_saving = (
    1 - optimized["energy_proxy"]
    / baseline["energy_proxy"]
) * 100

print("\n" + "=" * 75)
print("OSZCZĘDNOŚCI — WARIANT OPTYMALNY WZGLĘDEM NIEOPTYMALNEGO")
print("=" * 75)

print(f"Oszczędność czasu: {time_saving:.2f}%")
print(f"Oszczędność pamięci: {memory_saving:.2f}%")
print(f"Oszczędność proxy energii: {energy_saving:.2f}%")


# ============================================================
# 7. PORÓWNANIE WYNIKÓW BIZNESOWYCH
# ============================================================

print("\nWYNIKI ANALITYCZNE — PORÓWNANIE")

for result in results:
    print(f"\n{result['name']}:")
    print(result["result"].to_string(index=False))


# ============================================================
# 8. WALIDACJA RÓWNOWAŻNOŚCI WYNIKÓW
# ============================================================

def normalize_result(df):
    normalized = df.copy()

    normalized["revenue"] = normalized["revenue"].round(2)

    return (
        normalized[["category", "revenue"]]
        .sort_values("category")
        .reset_index(drop=True)
    )


# W pierwszych dwóch wariantach wynik kolumny revenue
# powstaje w Pandas; w trzecim w SQL.
for result in results:
    if result["result"].empty:
        raise ValueError(
            f"Pusty wynik strategii: {result['name']}"
        )

normalized_results = [
    normalize_result(result["result"])
    for result in results
]

if not normalized_results[0].equals(normalized_results[1]):
    raise ValueError(
        "Wyniki wariantu 1 i 2 różnią się."
    )

if not np.allclose(
    normalized_results[0]["revenue"].to_numpy(),
    normalized_results[2]["revenue"].to_numpy(),
    rtol=1e-9,
    atol=0.01
):
    raise ValueError(
        "Wyniki wariantu 1 i 3 różnią się."
    )

if any(
    result["rows_fetched"] < 0
    for result in results
):
    raise ValueError("Nieprawidłowa liczba pobranych rekordów.")

if any(
    result["memory_bytes"] <= 0
    for result in results
):
    raise ValueError("Nieprawidłowy pomiar pamięci.")

if any(
    result["average_time"] <= 0
    for result in results
):
    raise ValueError("Nieprawidłowy pomiar czasu.")

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print("Wszystkie trzy strategie zwróciły zgodne wyniki analityczne.")
print("Każda strategia pracowała na 500 000 transakcji.")
print("Każdy czas jest średnią z 3 pomiarów.")


# ============================================================
# 9. WNIOSKI — GREEN SQL
# ============================================================

print("\nWNIOSKI — GREEN SQL:")
print("1. SELECT powinien pobierać tylko potrzebne kolumny.")
print("2. Filtrowanie WHERE warto wykonywać w bazie danych.")
print("3. Indeksy mogą ograniczać zakres skanowanych danych.")
print("4. Agregacja GROUP BY w SQL ogranicza transfer do Pandas.")
print("5. LIMIT zmniejsza liczbę zwracanych rekordów.")
print("6. Mniejszy transfer i mniejsze zużycie pamięci")
print("   mogą ograniczać koszt obliczeń.")
print("7. Proxy czas × pamięć jest wskaźnikiem porównawczym,")
print("   a nie bezpośrednim pomiarem energii.")
