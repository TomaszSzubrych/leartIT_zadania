import pandas as pd


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Akumulatory dla przetwarzania partiami
total_passengers = 0
age_sum = 0.0
age_count = 0
survived_sum = 0

# Wczytywanie i przetwarzanie danych w partiach po 50 rekordow
for batch in pd.read_csv(url, chunksize=50):
    total_passengers += len(batch)

    age_sum += batch["Age"].sum()
    age_count += batch["Age"].count()

    survived_sum += batch["Survived"].sum()

# Wyniki przetwarzania partiami
avg_age = age_sum / age_count
survival_rate = survived_sum / total_passengers * 100

print("CUSTOM AGGREGATION - BATCH LOADING")
print("=" * 65)

print("\nWYNIKI PRZETWARZANIA PARTIAMI")
print("-" * 65)
print("total_passengers:", total_passengers)
print("avg_age:", round(avg_age, 2))
print("survival_rate:", f"{survival_rate:.2f}%")

# Porownanie z pelnym DataFrame
df = pd.read_csv(url)

full_total_passengers = len(df)
full_avg_age = df["Age"].mean()
full_survival_rate = df["Survived"].mean() * 100

print("\nWYNIKI DLA PELNEGO DATAFRAME")
print("-" * 65)
print("total_passengers:", full_total_passengers)
print("avg_age:", round(full_avg_age, 2))
print("survival_rate:", f"{full_survival_rate:.2f}%")

# Porownanie roznic
print("\nPOROWNANIE WYNIKOW")
print("-" * 65)

print(
    "Roznica liczby pasazerow:",
    total_passengers - full_total_passengers
)
print(
    "Roznica sredniego wieku:",
    round(avg_age - full_avg_age, 10)
)
print(
    "Roznica wskaznika przezycia:",
    round(survival_rate - full_survival_rate, 10),
    "punktow procentowych"
)
