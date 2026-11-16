import pandas as pd


# Wczytanie datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Sortowanie wedlug wieku rosnaco
df_posortowany = df.sort_values(by="Age", ascending=True)

# Usuniecie rekordow bez znanego wieku na potrzeby prezentacji
df_z_wiekiem = df_posortowany.dropna(subset=["Age"])

print("10 NAJMLODSZYCH PASAZEROW")
print("=" * 70)
print(df_z_wiekiem[["Name", "Age", "Sex"]].head(10).to_string(index=False))

print("\n10 NAJSTARSZYCH PASAZEROW")
print("=" * 70)
print(df_z_wiekiem[["Name", "Age", "Sex"]].tail(10).to_string(index=False))
