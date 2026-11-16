import pandas as pd
import numpy as np


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Wyznaczenie kwartylow i IQR
Q1 = df["Fare"].quantile(0.25)
Q3 = df["Fare"].quantile(0.75)
IQR = Q3 - Q1

# Granice wartosci normalnych
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identyfikacja wartosci odstajacych
outliers = df[
    (df["Fare"] < lower_bound) |
    (df["Fare"] > upper_bound)
]

# 1. Usuniecie wartosci odstajacych
df_removed = df[
    (df["Fare"] >= lower_bound) &
    (df["Fare"] <= upper_bound)
].copy()

# 2. Capping
df_capped = df.copy()
df_capped["Fare"] = np.clip(
    df_capped["Fare"],
    lower_bound,
    upper_bound
)

# 3. Transformacja logarytmiczna
df_log = df.copy()
df_log["Fare"] = np.log1p(df_log["Fare"])

print("OUTLIER DETECTION - FARE")
print("=" * 70)

print("\nGRANICE IQR")
print("-" * 70)
print(f"Q1: {Q1:.2f}")
print(f"Q3: {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"Dolna granica: {lower_bound:.2f}")
print(f"Gorna granica: {upper_bound:.2f}")

print("\nWARTOSCI ODSTAJACE")
print("-" * 70)
print("Liczba outlierow:", len(outliers))
print(f"Zakres wartosci normalnych: {lower_bound:.2f} - {upper_bound:.2f}")

print("\nPOROWNANIE DATAFRAME")
print("-" * 70)
print("Oryginalny zbior:", df.shape)
print("Po usunieciu outlierow:", df_removed.shape)
print("Po capping:", df_capped.shape)
print("Po transformacji log:", df_log.shape)

print("\n1. ORYGINALNE FARE")
print("-" * 70)
print(df["Fare"].describe())

print("\n2. FARE PO USUNIECIU OUTLIEROW")
print("-" * 70)
print(df_removed["Fare"].describe())

print("\n3. FARE PO CAPPING")
print("-" * 70)
print(df_capped["Fare"].describe())

print("\n4. FARE PO TRANSFORMACJI LOGARYTMICZNEJ")
print("-" * 70)
print(df_log["Fare"].describe())

print("\nWNIOSKI")
print("-" * 70)
print("Usuniecie outlierow zmniejsza liczbe rekordow.")
print("Capping zachowuje liczbe rekordow, ograniczajac skrajne wartosci.")
print("Log1p zmniejsza asymetrie rozkladu, zachowujac wszystkie rekordy.")
