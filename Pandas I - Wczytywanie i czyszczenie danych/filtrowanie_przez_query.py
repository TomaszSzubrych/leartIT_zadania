import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Filtrowanie przez query()
pierwsza_klasa = df.query("Pclass == 1 and Fare > 50")

# Obliczenie liczby pasazerow
liczba_pasazerow = len(pierwsza_klasa)

# Obliczenie sredniej ceny biletu
srednia_cena = pierwsza_klasa["Fare"].mean()

print("PASAZEROWIE PIERWSZEJ KLASY - BILETY POWYZEJ 50")
print("=" * 65)
print(f"Liczba pasazerow: {liczba_pasazerow}")
print(f"Srednia cena biletu: {srednia_cena:.2f}")

print("\nPierwsze 10 pasazerow spelniajacych warunki:")
print(pierwsza_klasa[["Name", "Pclass", "Fare"]].head(10).to_string(index=False))
