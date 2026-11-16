import pandas as pd


url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Wariant 1: pelne wczytanie danych
df_full = pd.read_csv(url)
memory_full = df_full.memory_usage(deep=True).sum() / 1024

# Wariant 2: wczytanie wybranych kolumn
wybrane_kolumny = ["Name", "Age", "Sex", "Pclass", "Survived"]

df_usecols = pd.read_csv(url, usecols=wybrane_kolumny)
memory_usecols = df_usecols.memory_usage(deep=True).sum() / 1024

# Wariant 3: przetwarzanie partiami po 100 rekordow
max_batch_memory = 0

for batch in pd.read_csv(url, chunksize=100):
    batch_memory = batch.memory_usage(deep=True).sum() / 1024
    max_batch_memory = max(max_batch_memory, batch_memory)

# Wariant 4: pelne wczytanie i optymalizacja typow danych
df_optimized = pd.read_csv(url)

kolumny_int8 = ["Pclass", "Survived", "SibSp", "Parch"]

for kolumna in kolumny_int8:
    df_optimized[kolumna] = df_optimized[kolumna].astype("int8")

kolumny_category = ["Sex", "Embarked"]

for kolumna in kolumny_category:
    df_optimized[kolumna] = df_optimized[kolumna].astype("category")

memory_optimized = (
    df_optimized.memory_usage(deep=True).sum() / 1024
)

# Zebranie wynikow
metody = [
    "Pelne wczytanie",
    "Wybrane kolumny (usecols)",
    "Batch loading (chunksize=100)",
    "Pelne + optymalizacja typow"
]

pamiec = [
    memory_full,
    memory_usecols,
    max_batch_memory,
    memory_optimized
]

results = pd.DataFrame({
    "Metoda": metody,
    "Pamiec (KB)": pamiec
})

# Oszczednosc wzgledem pelnego wczytania
results["Oszczednosc (%)"] = (
    (memory_full - results["Pamiec (KB)"]) / memory_full * 100
)

print("BENCHMARK EFEKTYWNOSCI PAMIECIOWEJ")
print("=" * 80)

print("\nTABELA POROWNAWCZA")
print("-" * 80)

print(
    results.to_string(
        index=False,
        formatters={
            "Pamiec (KB)": "{:.2f}".format,
            "Oszczednosc (%)": "{:.2f}%".format
        }
    )
)

# Tekstowe slupki: jeden blok = 10% maksymalnej pamieci
print("\nTEKSTOWA WIZUALIZACJA ZUZYCIA PAMIECI")
print("-" * 80)

for _, row in results.iterrows():
    liczba_blokow = round(
        row["Pamiec (KB)"] / memory_full * 10
    )

    pasek = "█" * liczba_blokow

    print(
        f"{row['Metoda']:35} "
        f"{pasek:10} "
        f"{row['Pamiec (KB)']:.2f} KB"
    )

# Szacowanie energii wedlug zalozenia dydaktycznego
print("\nSZACOWANE ZUZYCIE ENERGII")
print("-" * 80)
print("Zalozenie: 1 MB RAM ~= 0.0003 kWh/h")
print("Wyniki sa szacunkiem dydaktycznym, nie pomiarem energii.")

for _, row in results.iterrows():
    pamiec_mb = row["Pamiec (KB)"] / 1024
    energia = pamiec_mb * 0.0003

    print(
        f"{row['Metoda']:35} "
        f"{energia:.8f} kWh/h"
    )

print("\nPODSUMOWANIE")
print("-" * 80)
print("Najmniejsze zuzycie pamieci:")
print(results.loc[results["Pamiec (KB)"].idxmin(), "Metoda"])

print("Najwieksze zuzycie pamieci:")
print(results.loc[results["Pamiec (KB)"].idxmax(), "Metoda"])

print(
    "\nOszczednosc pamieci po optymalizacji typow:",
    f"{(memory_full - memory_optimized) / memory_full * 100:.2f}%"
)
