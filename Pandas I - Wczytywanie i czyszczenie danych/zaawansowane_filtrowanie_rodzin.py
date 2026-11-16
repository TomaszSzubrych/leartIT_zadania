import pandas as pd


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Utworzenie rozmiaru rodziny
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

# Utworzenie identyfikatora rodziny na podstawie nazwiska i rozmiaru
df["Surname"] = df["Name"].str.split(",").str[0].str.strip()
df["FamilyID"] = df["Surname"] + "_" + df["FamilySize"].astype(str)

# Filtrowanie rodzin wieloosobowych
rodziny = df[df["FamilySize"] > 1].copy()

# Grupowanie rodzin i obliczanie statystyk
analiza_rodzin = (
    rodziny.groupby("FamilyID")
    .agg(
        survival_rate=("Survived", "mean"),
        family_count=("Survived", "count")
    )
    .reset_index()
)

# Rodziny z co najmniej 50% wskaznikiem przezycia
szczesliwe_rodziny = analiza_rodzin[
    analiza_rodzin["survival_rate"] >= 0.50
].copy()

# Sortowanie wedlug liczebnosci i wybor 10 rodzin
top_10 = szczesliwe_rodziny.sort_values(
    by="family_count",
    ascending=False
).head(10)

print("ZAAWANSOWANE FILTROWANIE - ANALIZA RODZIN")
print("=" * 75)

print("\nPODSTAWOWE STATYSTYKI")
print("-" * 75)
print("Liczba wszystkich pasazerow:", len(df))
print("Liczba pasazerow w rodzinach wieloosobowych:", len(rodziny))
print("Liczba roznych rodzin wieloosobowych:", analiza_rodzin.shape[0])
print("Liczba rodzin z survival_rate >= 50%:", len(szczesliwe_rodziny))

print("\nTOP 10 NAJSZCZESLIWSZYCH RODZIN")
print("-" * 75)

wynik = top_10.copy()
wynik["survival_rate"] = wynik["survival_rate"] * 100

print(
    wynik.to_string(
        index=False,
        formatters={"survival_rate": "{:.2f}%".format}
    )
)
