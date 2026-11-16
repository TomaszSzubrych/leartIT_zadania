import pandas as pd


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# DataFrame boolean: True = NaN, False = wartosc
braki = df.isnull()

# Macierz korelacji miedzy brakami danych
matrix = braki.corr()

print("KORELACJA MIEDZY BRAKAMI DANYCH - TITANIC")
print("=" * 75)

print("\nMACIERZ KORELACJI")
print("-" * 75)
print(matrix.round(2))

print("\nNAJSILNIEJSZE DODATNIE KORELACJE")
print("-" * 75)

# Wyswietlenie par kolumn z dodatnia korelacja
for i, kolumna_1 in enumerate(matrix.columns):
    for kolumna_2 in matrix.columns[i + 1:]:
        korelacja = matrix.loc[kolumna_1, kolumna_2]

        if pd.notna(korelacja) and korelacja > 0:
            print(
                f"{kolumna_1} - {kolumna_2}: "
                f"{korelacja:.2f}"
            )

print("\nINTERPRETACJA")
print("-" * 75)
print("Korelacja dodatnia: braki w obu kolumnach czesciej wspolwystepuja.")
print("Korelacja bliska zeru: brak wyraznej zaleznosci liniowej.")
print("Korelacja ujemna: braki w jednej kolumnie rzadziej")
print("wystepuja razem z brakami w drugiej kolumnie.")
print("\nKorelacja nie dowodzi zaleznosci przyczynowo-skutkowej.")
