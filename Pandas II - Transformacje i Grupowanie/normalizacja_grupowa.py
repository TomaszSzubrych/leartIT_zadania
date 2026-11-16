import pandas as pd
import numpy as np

# ============================================================
# 1. FUNKCJA GENERUJĄCA CALIFORNIA HOUSING
# ============================================================

def make_california_housing(n=5000, seed=42):
    """Generuje syntetyczny dataset wzorowany na California Housing."""
    rng = np.random.default_rng(seed)

    latitude = rng.uniform(32.5, 41.5, n)
    longitude = rng.uniform(-123.5, -114.5, n)
    med_inc = rng.gamma(shape=2.0, scale=1.8, size=n) + 0.5
    house_age = rng.integers(1, 55, n)
    ave_rooms = rng.normal(5.5, 1.5, n).clip(1, 15)
    ave_bedrms = (ave_rooms * rng.uniform(0.15, 0.25, n)).clip(0.5, 5)
    population = rng.integers(50, 5000, n)
    ave_occup = rng.normal(3.0, 0.8, n).clip(1, 10)

    med_house_val = (
        med_inc * 0.6
        + (latitude - 36) * 0.15
        - (house_age / 100)
        + rng.normal(0, 0.3, n)
    ).clip(0.15, 5.0)

    return pd.DataFrame({
        "MedInc": med_inc.round(4),
        "HouseAge": house_age,
        "AveRooms": ave_rooms.round(4),
        "AveBedrms": ave_bedrms.round(4),
        "Population": population,
        "AveOccup": ave_occup.round(4),
        "Latitude": latitude.round(4),
        "Longitude": longitude.round(4),
        "MedHouseVal": med_house_val.round(4)
    })


# ============================================================
# 2. GENEROWANIE DATASETU
# ============================================================

df = make_california_housing()

print("=== CALIFORNIA HOUSING ===")
print(f"Liczba rekordów: {len(df)}")

# ============================================================
# 3. UTWORZENIE KOLUMNY REGION
# ============================================================

conditions = [
    (df["Latitude"] >= 36) & (df["Longitude"] >= -119),
    (df["Latitude"] >= 36) & (df["Longitude"] < -119),
    (df["Latitude"] < 36) & (df["Longitude"] >= -119),
    (df["Latitude"] < 36) & (df["Longitude"] < -119)
]

choices = ["NE", "NW", "SE", "SW"]

df["Region"] = np.select(
    conditions,
    choices,
    default="Unknown"
)

# ============================================================
# 4. FUNKCJA NORMALIZACJI MIN-MAX
# ============================================================

def min_max_normalization(x):
    return (x - x.min()) / (x.max() - x.min())


# ============================================================
# 5. NORMALIZACJA MEDINC W KAŻDYM REGIONIE
# ============================================================

df["MedInc_norm"] = (
    df
    .groupby("Region")["MedInc"]
    .transform(min_max_normalization)
)

# ============================================================
# 6. WERYFIKACJA MINIMUM I MAKSIMUM W REGIONACH
# ============================================================

verification = (
    df
    .groupby("Region")["MedInc_norm"]
    .agg(["min", "max"])
)

print("\n=== WERYFIKACJA NORMALIZACJI GRUPOWEJ ===")
print(verification.to_string())

# ============================================================
# 7. PODGLĄD DANYCH
# ============================================================

print("\n=== PRZYKŁADOWE DANE PO NORMALIZACJI ===")

print(
    df[["Region", "MedInc", "MedInc_norm"]]
    .head(10)
    .to_string(index=False)
)

