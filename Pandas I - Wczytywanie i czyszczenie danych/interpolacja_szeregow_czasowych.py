import pandas as pd
import numpy as np


# Utworzenie szeregu czasowego - 20 dni
daty = pd.date_range(start="2026-01-01", periods=20, freq="D")

# Wartosc None oznacza brak danych (NaN)
wartosci = [
    10, 12, np.nan, 16, 18,
    np.nan, 22, 24, np.nan, 28,
    30, np.nan, 34, 36, np.nan,
    40, 42, np.nan, 46, 48
]

df = pd.DataFrame({
    "Oryginal": wartosci
}, index=daty)

# Uzupelnianie brakow trzema metodami
df["ffill"] = df["Oryginal"].ffill()
df["bfill"] = df["Oryginal"].bfill()
df["interpolate"] = df["Oryginal"].interpolate(method="linear")

print("INTERPOLACJA SZEREGOW CZASOWYCH")
print("=" * 75)

print("\nTABELA POROWNAWCZA")
print(df.to_string())

# Tekstowa wizualizacja: jeden znak blokowy = 2 jednostki
print("\nWIZUALIZACJA TEKSTOWA")
print("Kazdy znak █ oznacza 2 jednostki")

kolumny = ["Oryginal", "ffill", "bfill", "interpolate"]

for kolumna in kolumny:
    print(f"\n{kolumna}:")
    for data, wartosc in df[kolumna].items():
        if pd.isna(wartosc):
            pasek = "NaN - brak danych"
        else:
            pasek = "█" * int(wartosc / 2)

        print(f"{data.strftime('%Y-%m-%d')}: {pasek}")

print("\nPODSUMOWANIE")
print("=" * 75)

print("Liczba brakow w oryginale:", df["Oryginal"].isnull().sum())

for kolumna in ["ffill", "bfill", "interpolate"]:
    print(
        f"Liczba brakow po {kolumna}: "
        f"{df[kolumna].isnull().sum()}"
    )
