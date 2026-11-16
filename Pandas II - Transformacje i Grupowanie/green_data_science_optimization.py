import pandas as pd
import numpy as np
import time

# ============================================================
# 1. GENEROWANIE DATASETU — 1 000 000 REKORDÓW
# ============================================================

np.random.seed(42)

N = 1_000_000

big_sales = pd.DataFrame({
    "Region": np.random.choice(
        ["North", "South", "East", "West"],
        N
    ),
    "Produkt": np.random.choice(
        list("ABCDE"),
        N
    ),
    "Sprzedaż": np.random.randint(10, 1000, N),
    "Koszt": np.random.randint(5, 500, N)
})

print("=== DATASET SPRZEDAŻY ===")
print(f"Liczba rekordów: {len(big_sales)}")
print(f"Liczba kolumn: {len(big_sales.columns)}")

# ============================================================
# 2. POMIAR PAMIĘCI PRZED OPTYMALIZACJĄ
# ============================================================

memory_before = (
    big_sales.memory_usage(deep=True).sum() / 1024**2
)

print("\n=== PAMIĘĆ PRZED OPTYMALIZACJĄ ===")
print(f"Pamięć przed: {memory_before:.2f} MB")

# ============================================================
# 3. FUNKCJA AGREGUJĄCA
# ============================================================

def aggregate_sales(data):
    return (
        data.groupby("Region", observed=True)
        .agg(
            Suma_Sprzedaży=("Sprzedaż", "sum"),
            Średnia_Sprzedaż=("Sprzedaż", "mean"),
            Suma_Kosztów=("Koszt", "sum"),
            Średni_Koszt=("Koszt", "mean")
        )
    )

# ============================================================
# 4. FUNKCJA POMIARU CZASU — ŚREDNIA Z 3 PRÓB
# ============================================================

def measure_aggregation_time(data, repetitions=3):
    times = []

    for _ in range(repetitions):
        start = time.perf_counter()

        result = aggregate_sales(data)

        end = time.perf_counter()

        times.append(end - start)

    return np.mean(times), times, result


# ============================================================
# 5. AGREGACJA PRZED OPTYMALIZACJĄ
# ============================================================

time_before, times_before, result_before = (
    measure_aggregation_time(big_sales)
)

print("\n=== AGREGACJA PRZED OPTYMALIZACJĄ ===")

for number, elapsed in enumerate(times_before, start=1):
    print(f"Próba {number}: {elapsed:.6f} s")

print(f"Średni czas przed: {time_before:.6f} s")

# ============================================================
# 6. OPTYMALIZACJA TYPÓW DANYCH
# ============================================================

big_sales["Region"] = big_sales["Region"].astype("category")
big_sales["Produkt"] = big_sales["Produkt"].astype("category")

big_sales["Sprzedaż"] = big_sales["Sprzedaż"].astype("int32")
big_sales["Koszt"] = big_sales["Koszt"].astype("int32")

print("\n=== TYPY DANYCH PO OPTYMALIZACJI ===")
print(big_sales.dtypes.to_string())

# ============================================================
# 7. POMIAR PAMIĘCI PO OPTYMALIZACJI
# ============================================================

memory_after = (
    big_sales.memory_usage(deep=True).sum() / 1024**2
)

memory_savings = (
    (memory_before - memory_after)
    / memory_before
    * 100
)

print("\n=== PAMIĘĆ PO OPTYMALIZACJI TYPÓW ===")
print(f"Pamięć po: {memory_after:.2f} MB")
print(f"Oszczędność pamięci: {memory_savings:.2f}%")

# ============================================================
# 8. AGREGACJA PO OPTYMALIZACJI
# ============================================================

time_after, times_after, result_after = (
    measure_aggregation_time(big_sales)
)

print("\n=== AGREGACJA PO OPTYMALIZACJI ===")

for number, elapsed in enumerate(times_after, start=1):
    print(f"Próba {number}: {elapsed:.6f} s")

print(f"Średni czas po: {time_after:.6f} s")

print("\n=== WYNIK AGREGACJI PO OPTYMALIZACJI ===")
print(result_after.round(2).to_string())

# ============================================================
# 9. PAMIĘĆ WYNIKU AGREGACJI
# ============================================================

aggregated_memory = (
    result_after.memory_usage(deep=True).sum()
    / 1024**2
)

print("\n=== PAMIĘĆ WYNIKU AGREGACJI ===")
print(f"Pamięć zagregowanego DataFrame: {aggregated_memory:.6f} MB")

# ============================================================
# 10. PORÓWNANIE CZASU
# ============================================================

time_difference = time_before - time_after

if time_before > 0:
    time_savings = (
        time_difference / time_before * 100
    )
else:
    time_savings = 0.0

print("\n=== PORÓWNANIE CZASU AGREGACJI ===")
print(f"Czas przed: {time_before:.6f} s")
print(f"Czas po:    {time_after:.6f} s")
print(f"Różnica:    {time_difference:.6f} s")
print(f"Zmiana:     {time_savings:.2f}%")

# ============================================================
# 11. RAPORT KOŃCOWY
# ============================================================

report = pd.DataFrame({
    "Metryka": [
        "Pamięć przed optymalizacją (MB)",
        "Pamięć po optymalizacji (MB)",
        "Oszczędność pamięci (%)",
        "Pamięć wyniku agregacji (MB)",
        "Średni czas przed (s)",
        "Średni czas po (s)",
        "Zmiana czasu (%)"
    ],
    "Wartość": [
        memory_before,
        memory_after,
        memory_savings,
        aggregated_memory,
        time_before,
        time_after,
        time_savings
    ]
})

print("\n=== RAPORT GREEN DATA SCIENCE ===")
print(report.round(4).to_string(index=False))

# ============================================================
# 12. WNIOSKI
# ============================================================

print("\n=== WNIOSKI ===")

print(
    f"Zmiana typów danych pozwoliła zaoszczędzić "
    f"{memory_savings:.2f}% pamięci."
)

if time_after < time_before:
    print(
        f"Agregacja po optymalizacji była szybsza "
        f"o {time_savings:.2f}%."
    )
elif time_after > time_before:
    print(
        f"Agregacja po optymalizacji była wolniejsza "
        f"o {abs(time_savings):.2f}%."
    )
else:
    print("Czas agregacji pozostał taki sam.")

if memory_savings >= 50:
    print("WYMAGANIE MINIMUM 50% OSZCZĘDNOŚCI SPEŁNIONE.")
else:
    print("WYMAGANIE MINIMUM 50% OSZCZĘDNOŚCI NIEZREALIZOWANE.")

# ============================================================
# 13. WERYFIKACJA KOŃCOWA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")

print(f"Liczba rekordów: {len(big_sales)}")
print(f"Liczba regionów: {big_sales['Region'].nunique()}")
print(f"Liczba produktów: {big_sales['Produkt'].nunique()}")

print(
    "Region category:",
    isinstance(big_sales["Region"].dtype, pd.CategoricalDtype)
)

print(
    "Produkt category:",
    isinstance(big_sales["Produkt"].dtype, pd.CategoricalDtype)
)

print(
    "Sprzedaż int32:",
    big_sales["Sprzedaż"].dtype == np.dtype("int32")
)

print(
    "Koszt int32:",
    big_sales["Koszt"].dtype == np.dtype("int32")
)

print(
    "Liczba regionów w agregacji:",
    len(result_after)
)

