import pandas as pd
import numpy as np

# ============================================================
# 1. GENEROWANIE DATASETU SPRZEDAŻY CZASOWEJ
# ============================================================

np.random.seed(42)

date_range = pd.date_range(
    start="2023-01-01",
    end="2023-12-31",
    freq="D"
)

sales_time = pd.DataFrame({
    "Data": date_range,
    "Sprzedaż": (
        np.random.poisson(lam=150, size=len(date_range))
        + np.sin(np.arange(len(date_range)) / 30) * 30
    )
})

print("=== DATASET SPRZEDAŻY CZASOWEJ ===")
print(f"Liczba rekordów: {len(sales_time)}")
print(f"Pierwsza data: {sales_time['Data'].min().date()}")
print(f"Ostatnia data: {sales_time['Data'].max().date()}")

# ============================================================
# 2. OBLICZENIE 7-DNIOWYCH STATYSTYK KROCZĄCYCH
# ============================================================

sales_time["rolling_mean"] = (
    sales_time["Sprzedaż"]
    .rolling(7)
    .mean()
)

sales_time["rolling_std"] = (
    sales_time["Sprzedaż"]
    .rolling(7)
    .std()
)

# ============================================================
# 3. WYKRYWANIE ANOMALII
# ============================================================

threshold = (
    sales_time["rolling_mean"]
    + 2 * sales_time["rolling_std"]
)

sales_time["anomaly"] = (
    sales_time["Sprzedaż"] > threshold
)

# ============================================================
# 4. TABELA — PIERWSZE 30 DNI
# ============================================================

print("\n=== ROLLING STATISTICS — PIERWSZE 30 DNI ===")

columns = [
    "Data",
    "Sprzedaż",
    "rolling_mean",
    "rolling_std",
    "anomaly"
]

print(
    sales_time[columns]
    .head(30)
    .round(2)
    .to_string(index=False)
)

# ============================================================
# 5. LISTA WSZYSTKICH ANOMALII
# ============================================================

anomalies = sales_time.loc[
    sales_time["anomaly"],
    columns
].copy()

print("\n=== WSZYSTKIE ANOMALIE ===")
print(f"Liczba anomalii: {len(anomalies)}")

if anomalies.empty:
    print("Nie wykryto anomalii.")
else:
    print(
        anomalies
        .round(2)
        .to_string(index=False)
    )

