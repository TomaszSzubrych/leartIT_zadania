import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Filtrowanie: wiek ponizej 18 lat i przezycie katastrofy
warunek = (df["Age"] < 18) & (df["Survived"] == 1)
mlodzi_ocaleni = df[warunek]

# Liczba osob spelniajacych oba warunki
liczba_osob = len(mlodzi_ocaleni)

print("MLODZI PASAZEROWIE, KTORZY PRZEZYLI")
print("=" * 65)
print(f"Liczba osob: {liczba_osob}")

# Wyswietlenie imion i wieku
print("\nImiona i wiek pasazerow:")
print(mlodzi_ocaleni[["Name", "Age"]].to_string(index=False))
