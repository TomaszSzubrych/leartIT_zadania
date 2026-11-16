import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Zachowanie statystyk Age przed czyszczeniem
statystyki_age_przed = df["Age"].describe()

print("KOMPLEKSOWE CZYSZCZENIE DATASETU TITANIC")
print("=" * 65)
print(f"Kształt przed czyszczeniem: {df.shape}")

# Usuniecie kolumn zawierajacych wiecej niz 60% NaN
procent_nan = (df.isnull().sum() / len(df)) * 100
kolumny_do_usuniecia = procent_nan[procent_nan > 60].index
df = df.drop(columns=kolumny_do_usuniecia)

print("\nUsuniete kolumny:")
print(list(kolumny_do_usuniecia))

# Uzupelnienie brakow w Age mediana
mediana_age = df["Age"].median()
df["Age"] = df["Age"].fillna(mediana_age)

# Uzupelnienie brakow w Embarked dominanta
dominanta_embarked = df["Embarked"].mode()[0]
df["Embarked"] = df["Embarked"].fillna(dominanta_embarked)

# Usuniecie wierszy z pozostalyymi brakujacymi wartosciami
df = df.dropna()

print("\nKształt po czyszczeniu:", df.shape)

# Sprawdzenie brakujacych wartosci
print("\nLiczba NaN po czyszczeniu:")
print(df.isnull().sum())

# Porownanie statystyk Age
print("\nSTATYSTYKI AGE PRZED CZYSZCZENIEM")
print(statystyki_age_przed)

print("\nSTATYSTYKI AGE PO CZYSZCZENIU")
print(df["Age"].describe())

print("\nLiczba rekordow po czyszczeniu:", len(df))
print("Liczba pozostalych brakujacych wartosci:", df.isnull().sum().sum())
