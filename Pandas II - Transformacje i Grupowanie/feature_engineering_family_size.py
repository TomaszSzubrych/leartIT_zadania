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
# 2. UTWORZENIE CECHY FAMILY_SIZE
# ============================================================

titanic["Family_Size"] = (
    titanic["SibSp"] + titanic["Parch"] + 1
)

print("\n=== ROZMIAR RODZINY ===")
print(titanic[["SibSp", "Parch", "Family_Size"]].head(10).to_string(index=False))

# ============================================================
# 3. OBLICZENIE SURVIVAL RATE WEDŁUG ROZMIARU RODZINY
# ============================================================

survival_rates = (
    titanic
    .groupby("Family_Size")["Survived"]
    .mean()
    .mul(100)
    .round(2)
)

print("\n=== SURVIVAL RATE WEDŁUG FAMILY_SIZE ===")

result = survival_rates.rename("Survival Rate (%)").to_frame()

print(result.to_string())

# ============================================================
# 4. IDENTYFIKACJA NAJWYŻSZEGO SURVIVAL RATE
# ============================================================

best_family_size = survival_rates.idxmax()
best_survival_rate = survival_rates.max()

print("\n=== NAJWYŻSZY SURVIVAL RATE ===")
print(f"Family_Size: {best_family_size}")
print(f"Survival Rate: {best_survival_rate:.2f}%")

# ============================================================
# 5. TEKSTOWE SŁUPKI PORÓWNUJĄCE WSZYSTKIE ROZMIARY
# ============================================================

print("\n=== PORÓWNANIE SURVIVAL RATE ===")
print("Legenda: █ = 2%")

for family_size, rate in survival_rates.items():
    bar = "█" * round(rate / 2)
    print(f"Rodzina {family_size:<2} {bar} {rate:.2f}%")

