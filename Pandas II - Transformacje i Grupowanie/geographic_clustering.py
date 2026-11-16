import pandas as pd
import numpy as np

# ============================================================
# 1. GENEROWANIE SYNTETYCZNEGO DATASETU CALIFORNIA HOUSING
# ============================================================

def make_california_housing(n=5000, seed=42):
    """Generuje syntetyczny dataset wzorowany na California Housing."""
    rng = np.random.default_rng(seed)

    latitude = rng.uniform(32.5, 41.5, n)
    longitude = rng.uniform(-123.5, -114.5, n)
    med_inc = rng.gamma(shape=2.0, scale=1.8, size=n) + 0.5
    house_age = rng.integers(1, 55, n)
    ave_rooms = rng.normal(5.5, 1.5, n).clip(1, 15)
    ave_bedrms = (
        ave_rooms * rng.uniform(0.15, 0.25, n)
    ).clip(0.5, 5)

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


df = make_california_housing()

print("=== CALIFORNIA HOUSING ===")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")

# ============================================================
# 2. PODZIAŁ KALIFORNII NA SIATKĘ 10 x 10
# ============================================================

df["lat_bin"], lat_edges = pd.cut(
    df["Latitude"],
    bins=10,
    retbins=True
)

df["lon_bin"], lon_edges = pd.cut(
    df["Longitude"],
    bins=10,
    retbins=True
)

df["Region"] = (
    df["lat_bin"].astype(str)
    + " | "
    + df["lon_bin"].astype(str)
)

# ============================================================
# 3. STATYSTYKI DLA KAŻDEGO REGIONU
# ============================================================

regional_stats = (
    df.groupby(
        ["lat_bin", "lon_bin", "Region"],
        observed=True
    )
    .agg(
        Avg_MedHouseVal=("MedHouseVal", "mean"),
        Median_MedInc=("MedInc", "median"),
        Total_Population=("Population", "sum"),
        Observations=("MedHouseVal", "size")
    )
    .reset_index()
)

regional_stats = regional_stats.sort_values(
    "Avg_MedHouseVal",
    ascending=False
)

print("\n=== STATYSTYKI REGIONÓW ===")
print(f"Liczba regionów z obserwacjami: {len(regional_stats)}")

print("\n=== TOP 10 NAJDROŻSZYCH REGIONÓW ===")
print(
    regional_stats[
        [
            "Region",
            "Avg_MedHouseVal",
            "Median_MedInc",
            "Total_Population",
            "Observations"
        ]
    ]
    .head(10)
    .round(4)
    .to_string(index=False)
)

print("\n=== TOP 10 NAJTAŃSZYCH REGIONÓW ===")
print(
    regional_stats[
        [
            "Region",
            "Avg_MedHouseVal",
            "Median_MedInc",
            "Total_Population",
            "Observations"
        ]
    ]
    .tail(10)
    .sort_values("Avg_MedHouseVal")
    .round(4)
    .to_string(index=False)
)

# ============================================================
# 4. TEKSTOWA HEATMAPA 10 x 10 — NP.HISTOGRAM2D
# ============================================================

# Suma cen w każdej komórce siatki.

price_sum, _, _ = np.histogram2d(
    df["Latitude"],
    df["Longitude"],
    bins=[lat_edges, lon_edges],
    weights=df["MedHouseVal"]
)

# Liczba obserwacji w każdej komórce.

observation_count, _, _ = np.histogram2d(
    df["Latitude"],
    df["Longitude"],
    bins=[lat_edges, lon_edges]
)

# Średnia cena w każdej komórce.

mean_price_grid = np.divide(
    price_sum,
    observation_count,
    out=np.full_like(price_sum, np.nan),
    where=observation_count > 0
)

# Kwartyle wyznaczamy na podstawie niepustych komórek.

valid_prices = mean_price_grid[
    ~np.isnan(mean_price_grid)
]

q1, q2, q3 = np.quantile(
    valid_prices,
    [0.25, 0.50, 0.75]
)

# Symbole reprezentujące kwartyle cen.

def price_symbol(value):
    if np.isnan(value):
        return "-"

    if value <= q1:
        return "."

    if value <= q2:
        return "·"

    if value <= q3:
        return "■"

    return "█"


# ============================================================
# 5. WYŚWIETLENIE HEATMAPY
# ============================================================

print("\n=== TEKSTOWA HEATMAPA 10 x 10 ===")
print("Legenda: █ = Q4 | ■ = Q3 | · = Q2 | . = Q1 | - = brak danych")

# Wyświetlamy szerokości geograficzne od najwyższej do najniższej.
# Długości geograficzne od zachodu do wschodu.

print("\nLatitude \\ Longitude")

for row_index in range(9, -1, -1):
    symbols = [
        price_symbol(mean_price_grid[row_index, col_index])
        for col_index in range(10)
    ]

    print(
        f"{row_index:2d} | "
        + " ".join(symbols)
    )

print("    " + "--" * 10)

# ============================================================
# 6. WERYFIKACJA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba komórek siatki: {mean_price_grid.size}")
print(f"Liczba niepustych komórek: {len(valid_prices)}")
print(f"Liczba pustych komórek: {np.isnan(mean_price_grid).sum()}")

print("\nKwartyle średnich cen regionów:")
print(f"Q1: {q1:.4f}")
print(f"Q2: {q2:.4f}")
print(f"Q3: {q3:.4f}")

if len(df) == 5000 and mean_price_grid.shape == (10, 10):
    print("\nGEOGRAPHIC CLUSTERING ZAKOŃCZONY POPRAWNIE.")
else:
    print("\nWERYFIKACJA WYKAZAŁA NIEPRAWIDŁOWOŚĆ.")

