import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# 1. Wielkosc rodziny
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

# 2. Informacja o samotnej podrozy
df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

# 3. Podzial pasazerow na grupy wiekowe
przedzialy = [0, 12, 18, 35, 60, float("inf")]
etykiety = ["0-12", "13-18", "19-35", "36-60", "60+"]

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=przedzialy,
    labels=etykiety,
    include_lowest=True
)

print("FEATURE ENGINEERING - DATASET TITANIC")
print("=" * 65)

print("\nWielkosc rodzin (FamilySize):")
print(df["FamilySize"].value_counts().sort_index())

print("\nPodrozowanie samotnie (IsAlone):")
print(df["IsAlone"].value_counts().sort_index())

print("\nGrupy wiekowe (AgeGroup):")
print(df["AgeGroup"].value_counts().sort_index())

# Wskaznik przezycia dla osob podrozujacych samotnie
wskaznik_samotnie = df.loc[df["IsAlone"] == 1, "Survived"].mean() * 100

# Wskaznik przezycia dla osob podrozujacych z rodzina
wskaznik_z_rodzina = df.loc[df["IsAlone"] == 0, "Survived"].mean() * 100

print("\nWSKAZNIK PRZEZYCIA")
print("=" * 65)
print(f"Osoby podrozujace samotnie: {wskaznik_samotnie:.2f}%")
print(f"Osoby podrozujace z rodzina: {wskaznik_z_rodzina:.2f}%")

print("\nPodglad nowych zmiennych:")
print(df[["Name", "FamilySize", "IsAlone", "Age", "AgeGroup"]].head(10))
