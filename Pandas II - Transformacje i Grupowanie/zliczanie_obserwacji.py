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
# 2. ZLICZANIE PASAŻERÓW W GRUPACH
# ============================================================

passenger_counts = (
    titanic
    .groupby(["Pclass", "Survived"])
    .size()
    .unstack(fill_value=0)
)

# Czytelniejsze nazwy kolumn
passenger_counts.columns = [
    "Nie_przeżyli",
    "Przeżyli"
]

# ============================================================
# 3. PREZENTACJA WYNIKÓW
# ============================================================

print("\n=== LICZBA PASAŻERÓW WEDŁUG KLASY I STATUSU PRZEŻYCIA ===")
print(passenger_counts.to_string())

print("\n=== SUMA PASAŻERÓW WEDŁUG KLASY ===")
print(passenger_counts.sum(axis=1).to_string())

print("\nŁączna liczba pasażerów:", passenger_counts.to_numpy().sum())

