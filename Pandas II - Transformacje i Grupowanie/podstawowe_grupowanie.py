import pandas as pd
import numpy as np

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

titanic = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(titanic)}")
print(f"Wymiary datasetu: {titanic.shape}")

# ============================================================
# 2. GRUPOWANIE WEDŁUG KLASY I PŁCI
# ============================================================

average_age = (
    titanic
    .groupby(["Pclass", "Sex"])["Age"]
    .mean()
    .reset_index(name="Średni_wiek")
)

# Zaokrąglenie średniego wieku do dwóch miejsc po przecinku
average_age["Średni_wiek"] = average_age["Średni_wiek"].round(2)

# ============================================================
# 3. PREZENTACJA WYNIKÓW
# ============================================================

print("\n=== ŚREDNI WIEK PASAŻERÓW WEDŁUG KLASY I PŁCI ===")
print(average_age.to_string(index=False))

print("\nLiczba kombinacji klasy i płci:", len(average_age))

