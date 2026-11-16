import pandas as pd
import numpy as np

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

titanic = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(titanic)}")

# ============================================================
# 2. PODZIAŁ PASAŻERÓW NA KATEGORIE WIEKOWE
# ============================================================

bins = [0, 12, 18, 60, float("inf")]
labels = ["Dziecko", "Nastolatek", "Dorosły", "Senior"]

titanic["Age_Category"] = pd.cut(
    titanic["Age"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# ============================================================
# 3. OBLICZENIE SURVIVAL RATE
# ============================================================

survival_rates = (
    titanic
    .groupby("Age_Category", observed=False)["Survived"]
    .mean()
    .mul(100)
    .round(2)
)

# ============================================================
# 4. PREZENTACJA WYNIKÓW — TABELA
# ============================================================

print("\n=== SURVIVAL RATE WEDŁUG KATEGORII WIEKOWYCH ===")

result = survival_rates.rename("Survival Rate (%)").to_frame()

print(result.to_string())

# ============================================================
# 5. TEKSTOWE SŁUPKI — JEDEN ZNAK = 2%
# ============================================================

print("\n=== TEKSTOWE SŁUPKI SURVIVAL RATE ===")
print("Legenda: █ = 2%")

for category, rate in survival_rates.items():
    bar = "█" * round(rate / 2)
    print(f"{category:<12} {bar} {rate:.2f}%")

