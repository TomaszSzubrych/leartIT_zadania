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

df_housing = make_california_housing()

print("=== CALIFORNIA HOUSING ===")
print(f"Liczba rekordów: {len(df_housing)}")

# ============================================================
# 3. UTWORZENIE KOLUMNY REGION
# ============================================================

conditions = [
    (df_housing["Latitude"] >= 36) & (df_housing["Longitude"] >= -119),
    (df_housing["Latitude"] >= 36) & (df_housing["Longitude"] < -119),
    (df_housing["Latitude"] < 36) & (df_housing["Longitude"] >= -119),
    (df_housing["Latitude"] < 36) & (df_housing["Longitude"] < -119)
]

choices = ["NE", "NW", "SE", "SW"]

df_housing["Region"] = np.select(
    conditions,
    choices,
    default="Unknown"
)

# ============================================================
# 4. WŁASNA FUNKCJA AGREGUJĄCA IQR
# ============================================================

def iqr_func(x):
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    return q3 - q1


# ============================================================
# 5. OBLICZENIE IQR WEDŁUG REGIONU
# ============================================================

regional_iqr = (
    df_housing
    .groupby("Region")["MedHouseVal"]
    .agg(iqr_func)
    .round(4)
    .sort_values(ascending=False)
)

# ============================================================
# 6. PREZENTACJA WYNIKÓW
# ============================================================

print("\n=== IQR MEDHOUSEVAL WEDŁUG REGIONU ===")
print(regional_iqr.to_string())


