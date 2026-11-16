import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Liczba brakujacych wartosci w kazdej kolumnie
liczba_nan = df.isnull().sum()

# Procent brakujacych wartosci
procent_nan = (df.isnull().sum() / len(df)) * 100

# Zestawienie wynikow
wyniki = pd.DataFrame({
    "Liczba NaN": liczba_nan,
    "Procent NaN": procent_nan
})

print("BRAKUJACE DANE W DATASECIE TITANIC")
print("=" * 65)

print("\nLiczba brakujacych wartosci w kazdej kolumnie:")
print(liczba_nan)

print("\nProcent brakujacych wartosci w kazdej kolumnie:")
print(procent_nan.round(2))

# Kolumny z wiecej niz 10% brakujacych danych
kolumny_z_brakami = wyniki[wyniki["Procent NaN"] > 10]

print("\nKOLUMNY Z WIECEJ NIZ 10% BRAKUJACYCH DANYCH:")
print(kolumny_z_brakami.round(2))
