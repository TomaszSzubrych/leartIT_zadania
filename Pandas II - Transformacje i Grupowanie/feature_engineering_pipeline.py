import pandas as pd
import numpy as np

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kolumn początkowych: {len(df.columns)}")

# ============================================================
# 2. UZUPEŁNIANIE BRAKÓW GRUPOWO
# ============================================================

print("\n=== BRAKI PRZED UZUPEŁNIENIEM ===")
print(df[["Age", "Fare"]].isna().sum().to_string())

df["Age"] = (
    df.groupby("Pclass")["Age"]
    .transform(lambda x: x.fillna(x.median()))
)

df["Fare"] = (
    df.groupby("Pclass")["Fare"]
    .transform(lambda x: x.fillna(x.median()))
)

# ============================================================
# 3. FEATURE ENGINEERING — FAMILY SIZE
# ============================================================

df["Family_Size"] = df["SibSp"] + df["Parch"] + 1

df["Is_Alone"] = (
    (df["SibSp"] + df["Parch"]) == 0
).astype(int)

# ============================================================
# 4. FEATURE ENGINEERING — TITLE
# ============================================================

df["Title"] = (
    df["Name"]
    .str.extract(r",\s*([^.]*)\.")[0]
    .str.strip()
)

# Kodowanie tytułów przez pd.factorize()

df["Title_Code"], title_categories = pd.factorize(df["Title"])

print("\n=== KATEGORIE TYTUŁÓW ===")
print(list(title_categories))

# ============================================================
# 5. FEATURE ENGINEERING — FARE PER PERSON
# ============================================================

df["Fare_Per_Person"] = (
    df["Fare"] / df["Family_Size"]
)

# ============================================================
# 6. FEATURE ENGINEERING — AGE GROUP
# ============================================================

age_bins = [0, 12, 18, 60, float("inf")]

age_labels = [
    "Dziecko",
    "Nastolatek",
    "Dorosły",
    "Senior"
]

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)

df["Age_Group_Code"] = df["Age_Group"].cat.codes

# ============================================================
# 7. AGREGACJA GRUPOWA — SURVIVAL RATE WEDŁUG TITLE
# ============================================================

df["Title_Survival_Rate"] = (
    df.groupby("Title")["Survived"]
    .transform("mean")
)

# ============================================================
# 8. KODOWANIE PŁCI
# ============================================================

df["Sex_Encoded"] = (
    df["Sex"].map({
        "male": 0,
        "female": 1
    })
)

# ============================================================
# 9. STANDARYZACJA GRUPOWA — MIN-MAX NIE, Z-SCORE
# ============================================================

def group_standardization(x):
    return (x - x.mean()) / x.std()

df["Age_Pclass_Std"] = (
    df.groupby("Pclass")["Age"]
    .transform(group_standardization)
)

df["Fare_Pclass_Std"] = (
    df.groupby("Pclass")["Fare"]
    .transform(group_standardization)
)

# ============================================================
# 10. WYBÓR CECH NUMERYCZNYCH
# ============================================================

feature_columns = [
    "Pclass",
    "Sex_Encoded",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Family_Size",
    "Is_Alone",
    "Fare_Per_Person",
    "Age_Group_Code",
    "Title_Code",
    "Title_Survival_Rate",
    "Age_Pclass_Std",
    "Fare_Pclass_Std"
]

# Zmienna docelowa pozostaje oddzielną kolumną.

df_ml = df[feature_columns + ["Survived"]].copy()

# ============================================================
# 11. WERYFIKACJA PIPELINE
# ============================================================

print("\n=== WYNIK FEATURE ENGINEERING PIPELINE ===")
print(f"Liczba rekordów: {len(df_ml)}")
print(f"Liczba cech: {len(feature_columns)}")
print(f"Liczba kolumn razem z targetem: {len(df_ml.columns)}")

print("\n=== PODGLĄD DATASETU ML ===")
print(df_ml.head(10).round(4).to_string(index=False))

print("\n=== TYPY DANYCH ===")
print(df_ml.dtypes.to_string())

print("\n=== BRAKUJĄCE WARTOŚCI ===")
print(df_ml.isna().sum().to_string())

print("\n=== WERYFIKACJA KOŃCOWA ===")

all_numeric = all(
    pd.api.types.is_numeric_dtype(dtype)
    for dtype in df_ml.dtypes
)

no_missing = df_ml.isna().sum().sum() == 0

print(f"Wszystkie kolumny numeryczne: {all_numeric}")
print(f"Brak brakujących wartości: {no_missing}")

if all_numeric and no_missing and len(feature_columns) >= 10:
    print("\nPIPELINE ZAKOŃCZONY POPRAWNIE.")
else:
    print("\nPIPELINE WYMAGA POPRAWY.")

