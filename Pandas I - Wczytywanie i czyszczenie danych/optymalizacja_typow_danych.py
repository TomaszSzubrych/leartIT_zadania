import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Pomiar pamieci przed optymalizacja
pamiec_przed = df.memory_usage(deep=True).sum()

# Optymalizacja typow liczbowych
kolumny_int8 = ["Pclass", "Survived", "SibSp", "Parch"]

for kolumna in kolumny_int8:
    df[kolumna] = df[kolumna].astype("int8")

# Optymalizacja kolumn tekstowych
kolumny_category = ["Sex", "Embarked"]

for kolumna in kolumny_category:
    df[kolumna] = df[kolumna].astype("category")

# Pomiar pamieci po optymalizacji
pamiec_po = df.memory_usage(deep=True).sum()

# Obliczenie procentowej redukcji pamieci
redukcja = ((pamiec_przed - pamiec_po) / pamiec_przed) * 100

print("OPTYMALIZACJA TYPOW DANYCH - TITANIC")
print("=" * 65)

print(f"Pamiec przed optymalizacja: {pamiec_przed:,} bajtow")
print(f"Pamiec po optymalizacji:    {pamiec_po:,} bajtow")
print(f"Zaoszczedzona pamiec:       {pamiec_przed - pamiec_po:,} bajtow")
print(f"Redukcja pamieci:           {redukcja:.2f}%")

print("\nTypy danych po optymalizacji:")
print(df.dtypes)

print("\nZuzycie pamieci poszczegolnych kolumn:")
print(df.memory_usage(deep=True))
