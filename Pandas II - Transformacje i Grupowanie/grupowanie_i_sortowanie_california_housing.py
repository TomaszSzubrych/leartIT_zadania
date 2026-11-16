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
print(f"Liczba kolumn: {len(df_housing.columns)}")

# ============================================================
# 3. PODZIAŁ KALIFORNII NA SIATKĘ 4 x 4
# ============================================================

df_housing["lat_bin"] = pd.cut(
    df_housing["Latitude"],
    bins=4
)

df_housing["lon_bin"] = pd.cut(
    df_housing["Longitude"],
    bins=4
)

df_housing["region"] = (
    df_housing["lat_bin"].astype(str)
    + "|"
    + df_housing["lon_bin"].astype(str)
)

# ============================================================
# 4. ŚREDNIA CENA DOMÓW WEDŁUG REGIONU
# ============================================================

regional_prices = (
    df_housing
    .groupby("region", observed=True)["MedHouseVal"]
    .mean()
    .sort_values(ascending=False)
)

# ============================================================
# 5. WYŚWIETLENIE TOP 5 REGIONÓW
# ============================================================

print("\n=== TOP 5 REGIONÓW — NAJWYŻSZA ŚREDNIA CENA DOMÓW ===")

top_5 = regional_prices.head(5).round(4)

print(top_5.to_string())

