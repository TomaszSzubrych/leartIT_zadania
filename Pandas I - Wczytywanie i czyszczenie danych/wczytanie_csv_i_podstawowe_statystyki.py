import pandas as pd


# Adres zbioru Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Wczytanie danych
df = pd.read_csv(url)

print("ANALIZA DATASETU TITANIC")
print("=" * 60)

print("\nPierwsze 5 wierszy:")
print(df.head())

print("\nInformacje o DataFrame:")
df.info()

print("\nStatystyki opisowe:")
print(df.describe())

print("\nSredni wiek pasazerow:")
print(f"{df['Age'].mean():.2f} lat")
