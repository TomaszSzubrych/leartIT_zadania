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
# 2. OBLICZENIE ŚREDNIEJ OPŁATY W KAŻDEJ KLASIE
# ============================================================

titanic["Avg_Fare_Pclass"] = (
    titanic
    .groupby("Pclass")["Fare"]
    .transform("mean")
)

# ============================================================
# 3. PREZENTACJA WYNIKÓW
# ============================================================

print("\n=== OPŁATA PASAŻERA I ŚREDNIA OPŁATA JEGO KLASY ===")

result = titanic[["Pclass", "Fare", "Avg_Fare_Pclass"]].head(10)

print(result.to_string(index=False))

print("\n=== ŚREDNIA OPŁATA WEDŁUG KLASY ===")
print(
    titanic
    .groupby("Pclass")["Avg_Fare_Pclass"]
    .first()
    .round(2)
    .to_string()
)

