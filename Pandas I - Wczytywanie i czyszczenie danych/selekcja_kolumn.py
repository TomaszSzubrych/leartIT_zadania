import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Wybor wymaganych kolumn
wybrane_kolumny = ["Name", "Age", "Sex", "Survived"]
df_subset = df[wybrane_kolumny].copy()

# Wyswietlenie pierwszych 10 wierszy
print("DATAFRAME - WYBRANE KOLUMNY")
print("=" * 70)
print(df_subset.head(10))

print("\nKsztalt nowego DataFrame:", df_subset.shape)

# Zapis do pliku CSV
plik_csv = "titanic_subset.csv"
df_subset.to_csv(plik_csv, index=False)

print(f"\nDane zapisano do pliku: {plik_csv}")
print("Liczba zapisanych rekordow:", len(df_subset))
