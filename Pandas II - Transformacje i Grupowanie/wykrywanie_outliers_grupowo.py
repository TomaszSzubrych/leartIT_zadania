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
# 4. WYKRYWANIE OUTLIERS METODĄ IQR
# ============================================================

def detect_outliers(group):
    q1 = group["MedHouseVal"].quantile(0.25)
    q3 = group["MedHouseVal"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        (group["MedHouseVal"] < lower_bound)
        | (group["MedHouseVal"] > upper_bound)
    )

    return pd.Series({
        "Outliers": int(outliers.sum()),
        "Min": group["MedHouseVal"].min(),
        "Q1": q1,
        "Median": group["MedHouseVal"].median(),
        "Q3": q3,
        "Max": group["MedHouseVal"].max()
    })


# ============================================================
# 5. OBLICZENIA DLA KAŻDEGO REGIONU
# ============================================================

regional_stats = (
    df
    .groupby("Region")
    .apply(detect_outliers, include_groups=False)
    .round(4)
)

print("\n=== LICZBA OUTLIERS WEDŁUG REGIONU ===")
print(regional_stats[["Outliers"]].to_string())

# ============================================================
# 6. TEKSTOWY BOXPLOT PIĘCIOPUNKTOWY
# ============================================================

print("\n=== TEKSTOWY BOXPLOT DLA KAŻDEGO REGIONU ===")
print("Format: min | Q1 | mediana | Q3 | max")

for region, row in regional_stats.iterrows():
    print(f"\nRegion: {region}")
    print(
        f"min={row['Min']:.4f} | "
        f"Q1={row['Q1']:.4f} | "
        f"med={row['Median']:.4f} | "
        f"Q3={row['Q3']:.4f} | "
        f"max={row['Max']:.4f}"
    )

