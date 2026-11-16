import pandas as pd

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

titanic = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(titanic)}")

# ============================================================
# 2. POMOCNICZY DATAFRAME Z PORTAMI
# ============================================================

ports = pd.DataFrame({
    "Embarked": ["S", "C", "Q"],
    "Port_Name": ["Southampton", "Cherbourg", "Queenstown"],
    "Country": ["UK", "France", "Ireland"],
    "Port_Size": ["Large", "Medium", "Small"]
})

print("\n=== INFORMACJE O PORTACH ===")
print(ports.to_string(index=False))

# ============================================================
# 3. POŁĄCZENIE DATASETÓW
# ============================================================

df = pd.merge(
    titanic,
    ports,
    on="Embarked",
    how="left"
)

# Zachowanie pasażerów bez informacji o porcie.

df[["Port_Name", "Country", "Port_Size"]] = (
    df[["Port_Name", "Country", "Port_Size"]]
    .fillna("Unknown")
)

print("\n=== POŁĄCZONE DATASETY ===")
print(f"Liczba rekordów po merge: {len(df)}")
print(f"Liczba kolumn po merge: {len(df.columns)}")

print("\n=== PODGLĄD POŁĄCZONYCH DANYCH ===")

print(
    df[
        [
            "PassengerId",
            "Embarked",
            "Port_Name",
            "Country",
            "Port_Size",
            "Age",
            "Fare",
            "Survived"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 4. AGREGACJA STATYSTYK WEDŁUG PORTU
# ============================================================

port_stats = (
    df.groupby(
        ["Port_Name", "Country", "Port_Size"]
    )
    .agg(
        Avg_Age=("Age", "mean"),
        Survival_Rate=("Survived", "mean"),
        Avg_Fare=("Fare", "mean"),
        Passengers=("PassengerId", "count")
    )
    .reset_index()
)

port_stats["Survival_Rate_%"] = (
    port_stats["Survival_Rate"] * 100
)

port_stats = port_stats.drop(
    columns=["Survival_Rate"]
)

print("\n=== STATYSTYKI WEDŁUG PORTU ===")

print(
    port_stats
    .round(2)
    .to_string(index=False)
)

# ============================================================
# 5. ANALIZA WEDŁUG ROZMIARU PORTU
# ============================================================

size_stats = (
    df.groupby("Port_Size")
    .agg(
        Avg_Age=("Age", "mean"),
        Survival_Rate=("Survived", "mean"),
        Avg_Fare=("Fare", "mean"),
        Passengers=("PassengerId", "count")
    )
    .reset_index()
)

size_stats["Survival_Rate_%"] = (
    size_stats["Survival_Rate"] * 100
)

size_stats = size_stats.drop(
    columns=["Survival_Rate"]
)

print("\n=== STATYSTYKI WEDŁUG ROZMIARU PORTU ===")

print(
    size_stats
    .round(2)
    .to_string(index=False)
)

# ============================================================
# 6. PORÓWNANIE PORTÓW POD WZGLĘDEM PRZEŻYWALNOŚCI
# ============================================================

known_ports = port_stats[
    port_stats["Port_Size"] != "Unknown"
].copy()

best_port = known_ports.loc[
    known_ports["Survival_Rate_%"].idxmax()
]

worst_port = known_ports.loc[
    known_ports["Survival_Rate_%"].idxmin()
]

print("\n=== PORÓWNANIE PRZEŻYWALNOŚCI PORTÓW ===")

print(
    f"Najwyższy survival rate: {best_port['Port_Name']} "
    f"({best_port['Survival_Rate_%']:.2f}%)"
)

print(
    f"Najniższy survival rate: {worst_port['Port_Name']} "
    f"({worst_port['Survival_Rate_%']:.2f}%)"
)

# ============================================================
# 7. WNIOSKI DOTYCZĄCE ROZMIARU PORTU
# ============================================================

known_sizes = size_stats[
    size_stats["Port_Size"] != "Unknown"
].copy()

largest_survival = known_sizes.loc[
    known_sizes["Survival_Rate_%"].idxmax()
]

smallest_survival = known_sizes.loc[
    known_sizes["Survival_Rate_%"].idxmin()
]

print("\n=== WNIOSKI — ROZMIAR PORTU A PRZEŻYWALNOŚĆ ===")

print(
    f"Najwyższy survival rate odnotowano dla kategorii "
    f"{largest_survival['Port_Size']}: "
    f"{largest_survival['Survival_Rate_%']:.2f}%."
)

print(
    f"Najniższy survival rate odnotowano dla kategorii "
    f"{smallest_survival['Port_Size']}: "
    f"{smallest_survival['Survival_Rate_%']:.2f}%."
)

print(
    "\nPorównanie ma charakter opisowy. "
    "Nie oznacza, że rozmiar portu powodował różnice "
    "w przeżywalności pasażerów."
)

# ============================================================
# 8. WERYFIKACJA KOŃCOWA
# ============================================================

print("\n=== WERYFIKACJA KOŃCOWA ===")

print(f"Liczba rekordów przed merge: {len(titanic)}")
print(f"Liczba rekordów po merge: {len(df)}")

print(
    "Liczba portów w tabeli pomocniczej:",
    len(ports)
)

print(
    "Liczba pasażerów z nieznanym portem:",
    (df["Port_Name"] == "Unknown").sum()
)

print(
    "Brak brakujących nazw portów:",
    df["Port_Name"].isna().sum() == 0
)

print(
    "Wszystkie rekordy zachowane:",
    len(titanic) == len(df)
)

