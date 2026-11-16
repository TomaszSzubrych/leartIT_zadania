import pandas as pd
import numpy as np

# ============================================================
# 1. GENEROWANIE SYNTETYCZNEGO DATASETU SPRZEDAŻY
# ============================================================

np.random.seed(42)

sales = pd.DataFrame({
    "Region": np.random.choice(["A", "B", "C"], 100),
    "Sprzedaż": np.random.randint(50, 500, 100)
})

print("=== DATASET SPRZEDAŻY ===")
print(sales.head(10).to_string(index=False))
print(f"\nLiczba rekordów: {len(sales)}")

# ============================================================
# 2. AGREGACJA STATYSTYK WEDŁUG REGIONU
# ============================================================

regional_stats = (
    sales
    .groupby("Region")["Sprzedaż"]
    .agg(["min", "max", "mean", "std"])
    .round(2)
)

# ============================================================
# 3. PREZENTACJA WYNIKÓW
# ============================================================

print("\n=== STATYSTYKI SPRZEDAŻY WEDŁUG REGIONU ===")
print(regional_stats.to_string())

