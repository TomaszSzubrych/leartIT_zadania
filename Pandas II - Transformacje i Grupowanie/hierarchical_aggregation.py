import pandas as pd
import numpy as np

# ============================================================
# 1. KONFIGURACJA DANYCH SYNTETYCZNYCH
# ============================================================

np.random.seed(42)

locations = {
    "Europa": {
        "Polska": ["Warszawa", "Kraków", "Gdańsk"],
        "Niemcy": ["Berlin", "Monachium", "Hamburg"],
        "Francja": ["Paryż", "Lyon", "Marsylia"]
    },
    "Azja": {
        "Japonia": ["Tokio", "Osaka", "Kioto"],
        "Chiny": ["Pekin", "Szanghaj", "Kanton"],
        "Indie": ["Delhi", "Mumbaj", "Bengaluru"]
    },
    "Ameryka Północna": {
        "USA": ["Nowy Jork", "Los Angeles", "Chicago"],
        "Kanada": ["Toronto", "Vancouver", "Montreal"],
        "Meksyk": ["Meksyk", "Guadalajara", "Monterrey"]
    }
}

# ============================================================
# 2. GENEROWANIE DATASETU SPRZEDAŻY
# ============================================================

records = []

for continent, countries in locations.items():
    for country, cities in countries.items():
        for city in cities:
            sales_values = np.random.randint(100, 1001, size=50)

            for sale in sales_values:
                records.append({
                    "Kontynent": continent,
                    "Kraj": country,
                    "Miasto": city,
                    "Sprzedaż": sale
                })

df = pd.DataFrame(records)

print("=== DATASET SPRZEDAŻY MIĘDZYNARODOWEJ ===")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kontynentów: {df['Kontynent'].nunique()}")
print(f"Liczba krajów: {df[['Kontynent', 'Kraj']].drop_duplicates().shape[0]}")
print(f"Liczba miast: {df[['Kontynent', 'Kraj', 'Miasto']].drop_duplicates().shape[0]}")

print("\n=== PRZYKŁADOWE REKORDY ===")
print(df.head(10).to_string(index=False))

# ============================================================
# 3. AGREGACJA — POZIOM KONTYNENTU
# ============================================================

continent_stats = (
    df.groupby("Kontynent")["Sprzedaż"]
    .sum()
    .reset_index(name="Sprzedaż")
)

continent_stats["Udział_%"] = (
    continent_stats["Sprzedaż"]
    / df["Sprzedaż"].sum()
    * 100
)

# ============================================================
# 4. AGREGACJA — POZIOM KRAJU
# ============================================================

country_stats = (
    df.groupby(["Kontynent", "Kraj"])["Sprzedaż"]
    .sum()
    .reset_index()
)

country_stats["Udział_%"] = (
    country_stats["Sprzedaż"]
    / country_stats["Kontynent"].map(
        continent_stats.set_index("Kontynent")["Sprzedaż"]
    )
    * 100
)

# ============================================================
# 5. AGREGACJA — POZIOM MIASTA
# ============================================================

city_stats = (
    df.groupby(["Kontynent", "Kraj", "Miasto"])["Sprzedaż"]
    .sum()
    .reset_index()
)

city_stats["Udział_%"] = (
    city_stats["Sprzedaż"]
    / city_stats["Kraj"].map(
        country_stats.set_index("Kraj")["Sprzedaż"]
    )
    * 100
)

# ============================================================
# 6. PREZENTACJA TRZECH POZIOMÓW AGREGACJI
# ============================================================

print("\n=== AGREGACJA — KONTYNENTY ===")
print(
    continent_stats.round(2).to_string(index=False)
)

print("\n=== AGREGACJA — KRAJE ===")
print(
    country_stats.round(2).to_string(index=False)
)

print("\n=== AGREGACJA — MIASTA ===")
print(
    city_stats.round(2).to_string(index=False)
)

# ============================================================
# 7. TEKSTOWE DRZEWO HIERARCHII
# ============================================================

print("\n=== DRZEWO SPRZEDAŻY: KONTYNENT → KRAJ → MIASTO ===")

for _, continent_row in continent_stats.iterrows():

    continent = continent_row["Kontynent"]

    print(
        f"{continent} | "
        f"Sprzedaż: {continent_row['Sprzedaż']:.0f} | "
        f"Udział: {continent_row['Udział_%']:.2f}%"
    )

    countries = country_stats[
        country_stats["Kontynent"] == continent
    ]

    for _, country_row in countries.iterrows():

        country = country_row["Kraj"]

        print(
            f"  ├── {country} | "
            f"Sprzedaż: {country_row['Sprzedaż']:.0f} | "
            f"Udział: {country_row['Udział_%']:.2f}%"
        )

        cities = city_stats[
            (city_stats["Kontynent"] == continent)
            & (city_stats["Kraj"] == country)
        ]

        for _, city_row in cities.iterrows():

            print(
                f"      ├── {city_row['Miasto']} | "
                f"Sprzedaż: {city_row['Sprzedaż']:.0f} | "
                f"Udział: {city_row['Udział_%']:.2f}%"
            )

# ============================================================
# 8. WERYFIKACJA KOŃCOWA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")

print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kontynentów: {len(continent_stats)}")
print(f"Liczba krajów: {len(country_stats)}")
print(f"Liczba miast: {len(city_stats)}")

print(
    "Suma udziałów kontynentów:",
    f"{continent_stats['Udział_%'].sum():.2f}%"
)

print(
    "Suma udziałów krajów w kontynentach:",
    country_stats.groupby("Kontynent")["Udział_%"].sum().round(2).to_dict()
)

print(
    "Suma udziałów miast w krajach:",
    city_stats.groupby(["Kontynent", "Kraj"])["Udział_%"].sum().round(2).to_dict()
)

