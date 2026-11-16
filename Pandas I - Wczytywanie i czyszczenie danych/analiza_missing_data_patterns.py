import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# DataFrame boolean: True oznacza NaN, False oznacza wartosc
braki = df.isnull()

print("ANALIZA MISSING DATA PATTERNS - TITANIC")
print("=" * 75)

# 1. Tekstowa mapa brakujacych danych - pierwsze 30 wierszy
print("\nTEKSTOWA MAPA BRAKUJACYCH DANYCH")
print("X = NaN, . = wartosc")
print("-" * 75)

kolumny = list(df.columns)

print("     " + " ".join(f"{kolumna[:10]:10}" for kolumna in kolumny))

for indeks in range(30):
    symbole = [
        "X" if braki.iloc[indeks][kolumna] else "."
        for kolumna in kolumny
    ]

    print(f"{indeks:3}  " + " ".join(f"{symbol:10}" for symbol in symbole))

# 2. Liczba wspolnych brakow
age_cabin = (braki["Age"] & braki["Cabin"]).sum()
age_embarked = (braki["Age"] & braki["Embarked"]).sum()

print("\nWSPOLNE BRAKUJACE WARTOSCI")
print("-" * 75)
print(f"NaN w Age i jednoczesnie NaN w Cabin: {age_cabin}")
print(f"NaN w Age i jednoczesnie NaN w Embarked: {age_embarked}")

# 3. Wskaznik przezycia dla osob z brakujacym wiekiem
przezycie_nan_age = df.loc[braki["Age"], "Survived"].mean() * 100

# Wskaznik przezycia dla osob z uzupelnionym wiekiem
przezycie_age = df.loc[~braki["Age"], "Survived"].mean() * 100

print("\nWSKAZNIK PRZEZYCIA")
print("-" * 75)
print(f"Pasazerowie z NaN w Age: {przezycie_nan_age:.2f}%")
print(f"Pasazerowie bez NaN w Age: {przezycie_age:.2f}%")

# 4. Podsumowanie liczby brakow
print("\nLICZBA BRAKUJACYCH WARTOSCI W KOLUMNACH")
print("-" * 75)
print(braki.sum())

print("\nWNIOSKI")
print("-" * 75)
print(
    "Wspolne braki Age i Cabin:",
    age_cabin,
    "przypadkow."
)
print(
    "Wspolne braki Age i Embarked:",
    age_embarked,
    "przypadkow."
)
print(
    "Roznica wskaznikow przezycia:",
    f"{abs(przezycie_nan_age - przezycie_age):.2f}",
    "punktow procentowych."
)
