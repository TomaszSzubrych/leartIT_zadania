import pandas as pd
import numpy as np

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(df)}")

# ============================================================
# 2. PRZYGOTOWANIE ZMIENNEJ EMBARKED
# ============================================================

df["Embarked"] = df["Embarked"].fillna("Unknown")

# ============================================================
# 3. NAIWNY TARGET ENCODING — CAŁY DATASET
# ============================================================

df["Embarked_Target_Naive"] = (
    df.groupby("Embarked")["Survived"]
    .transform("mean")
)

# ============================================================
# 4. LOSOWY PODZIAŁ NA 5 FOLDÓW
# ============================================================

np.random.seed(42)

permutation = np.random.permutation(len(df))

folds = np.array_split(permutation, 5)

df["Fold"] = -1

for fold_number, fold_indices in enumerate(folds):
    df.loc[fold_indices, "Fold"] = fold_number

print("\n=== PODZIAŁ NA FOLDY ===")

for fold_number, fold_indices in enumerate(folds):
    print(
        f"Fold {fold_number}: "
        f"{len(fold_indices)} rekordów"
    )

# ============================================================
# 5. TARGET ENCODING — OUT-OF-FOLD
# ============================================================

df["Embarked_Target"] = np.nan

for fold_number, validation_indices in enumerate(folds):

    # Indeksy pozostałych czterech foldów.
    training_indices = np.concatenate([
        fold
        for number, fold in enumerate(folds)
        if number != fold_number
    ])

    # Dane treningowe — bez obserwacji z walidowanego foldu.
    training_data = df.loc[training_indices]

    # Średni survival rate dla każdej kategorii Embarked.
    target_mapping = (
        training_data
        .groupby("Embarked")["Survived"]
        .mean()
    )

    # Średnia globalna z danych treningowych jako wartość
    # zastępcza dla kategorii nieobecnych w treningu.
    global_mean = training_data["Survived"].mean()

    # Przypisanie kodowania wyłącznie do pominiętego foldu.
    encoded_values = (
        df.loc[validation_indices, "Embarked"]
        .map(target_mapping)
        .fillna(global_mean)
    )

    df.loc[validation_indices, "Embarked_Target"] = (
        encoded_values
    )

# ============================================================
# 6. PORÓWNANIE KORELACJI
# ============================================================

naive_correlation = df[
    ["Embarked_Target_Naive", "Survived"]
].corr().iloc[0, 1]

oof_correlation = df[
    ["Embarked_Target", "Survived"]
].corr().iloc[0, 1]

comparison = pd.DataFrame({
    "Metoda": [
        "Naive Target Encoding",
        "Out-of-Fold Target Encoding"
    ],
    "Korelacja z Survived": [
        naive_correlation,
        oof_correlation
    ]
})

print("\n=== PORÓWNANIE KORELACJI ===")
print(comparison.round(4).to_string(index=False))

# ============================================================
# 7. PORÓWNANIE ROZKŁADU ENCODINGU
# ============================================================

print("\n=== ROZKŁAD NAIVE TARGET ENCODING ===")

print(
    df.groupby("Embarked")["Embarked_Target_Naive"]
    .agg(["mean", "min", "max", "count"])
    .round(4)
    .to_string()
)

print("\n=== ROZKŁAD OUT-OF-FOLD TARGET ENCODING ===")

print(
    df.groupby("Embarked")["Embarked_Target"]
    .agg(["mean", "min", "max", "count"])
    .round(4)
    .to_string()
)

# ============================================================
# 8. PODGLĄD DATAFRAME
# ============================================================

print("\n=== PODGLĄD TARGET ENCODING ===")

print(
    df[
        [
            "Embarked",
            "Survived",
            "Fold",
            "Embarked_Target",
            "Embarked_Target_Naive"
        ]
    ]
    .head(15)
    .round(4)
    .to_string(index=False)
)

# ============================================================
# 9. WERYFIKACJA KOŃCOWA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")

print(
    "Brak braków w Embarked_Target:",
    df["Embarked_Target"].isna().sum() == 0
)

print(
    "Wszystkie rekordy przypisane do foldów:",
    (df["Fold"] >= 0).all()
)

print(
    "Liczba foldów:",
    df["Fold"].nunique()
)

