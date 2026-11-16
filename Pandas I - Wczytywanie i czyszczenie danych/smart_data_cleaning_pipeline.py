import pandas as pd


def clean_titanic(df):
    # Praca na kopii - oryginalny DataFrame pozostaje bez zmian
    cleaned = df.copy()

    # Usuniecie kolumn zawierajacych ponad 60% brakow
    missing_ratio = cleaned.isnull().mean()
    kolumny_do_usuniecia = missing_ratio[
        missing_ratio > 0.60
    ].index

    cleaned = cleaned.drop(columns=kolumny_do_usuniecia)

    # Uzupelnienie brakujacego wieku mediana
    age_median = cleaned["Age"].median()
    cleaned["Age"] = cleaned["Age"].fillna(age_median)

    # Uzupelnienie brakujacego portu dominanta
    embarked_mode = cleaned["Embarked"].mode()[0]
    cleaned["Embarked"] = cleaned["Embarked"].fillna(embarked_mode)

    # Optymalizacja typow danych
    kolumny_int8 = ["Pclass", "Survived", "SibSp", "Parch"]

    for kolumna in kolumny_int8:
        cleaned[kolumna] = cleaned[kolumna].astype("int8")

    kolumny_category = ["Sex", "Embarked"]

    for kolumna in kolumny_category:
        cleaned[kolumna] = cleaned[kolumna].astype("category")

    # Dodanie rozmiaru rodziny
    cleaned["FamilySize"] = cleaned["SibSp"] + cleaned["Parch"] + 1

    return cleaned


# Wczytanie surowego zbioru Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# Zachowanie informacji o oryginalnym zbiorze
oryginalny_ksztalt = titanic.shape
oryginalne_braki = titanic.isnull().sum().sum()

# Uruchomienie funkcji czyszczacej
cleaned_titanic = clean_titanic(titanic)

print("SMART DATA CLEANING PIPELINE")
print("=" * 70)

print("\nINFORMACJE O OCZYSZCZONYM DATAFRAME")
print("-" * 70)
cleaned_titanic.info()

print("\nPODSUMOWANIE CZYSZCZENIA")
print("-" * 70)
print("Oryginalny ksztalt:", oryginalny_ksztalt)
print("Oczyszczony ksztalt:", cleaned_titanic.shape)
print("Braki w oryginalnym zbiorze:", oryginalne_braki)
print(
    "Braki w oczyszczonym zbiorze:",
    cleaned_titanic.isnull().sum().sum()
)
print("Kolumny oczyszczonego zbioru:")
print(cleaned_titanic.columns.tolist())

# Kontrola, czy funkcja nie zmienila oryginalu
print("\nKONTROLA ORYGINALNEGO DATAFRAME")
print("-" * 70)
print("Ksztalt oryginalnego zbioru:", titanic.shape)
print("Liczba brakow w oryginalnym zbiorze:",
      titanic.isnull().sum().sum())
print("Czy FamilySize istnieje w oryginale:", "FamilySize" in titanic.columns)
