import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Obliczenie sredniego wieku z pominięciem NaN
sredni_wiek = df["Age"].mean()

# Uzupelnienie brakujacych wartosci srednia
df["Age"] = df["Age"].fillna(sredni_wiek)

# Sprawdzenie brakujacych wartosci po uzupelnieniu
liczba_nan_po = df["Age"].isnull().sum()

print("UZUPEŁNIANIE BRAKUJĄCYCH WARTOŚCI AGE")
print("=" * 60)
print(f"Sredni wiek przed uzupelnieniem: {sredni_wiek:.2f}")
print(f"Liczba brakow po uzupelnieniu: {liczba_nan_po}")
print(f"Liczba uzupelnionych wartosci: {df['Age'].notnull().sum() - 714}")

print("\nStatystyki kolumny Age po uzupelnieniu:")
print(df["Age"].describe())

if liczba_nan_po == 0:
    print("\nWALIDACJA: Wszystkie braki w kolumnie Age zostaly uzupelnione.")
else:
    print("\nWALIDACJA: Nadal wystepuja brakujace wartosci.")
