import pandas as pd


# Adres datasetu Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Akumulatory dla globalnej sredniej wieku
age_sum = 0
age_count = 0

# Numer przetwarzanego batcha
numer_batcha = 0

print("BATCH PROCESSING - DATASET TITANIC")
print("=" * 65)

# Wczytywanie danych partiami po 100 wierszy
for batch in pd.read_csv(url, chunksize=100):
    numer_batcha += 1

    # Pominiecie brakujacych wartosci Age
    wiek = batch["Age"].dropna()

    # Sredni wiek w aktualnym batchu
    sredni_wiek = wiek.mean()

    print(f"Batch {numer_batcha}: sredni wiek = {sredni_wiek:.2f}")

    # Aktualizacja globalnych akumulatorow
    age_sum += wiek.sum()
    age_count += wiek.count()

# Globalna srednia ze wszystkich batchy
globalna_srednia = age_sum / age_count

print("\nPODSUMOWANIE")
print("=" * 65)
print(f"Liczba batchy: {numer_batcha}")
print(f"Liczba pasazerow z podanym wiekiem: {age_count}")
print(f"Suma wieku: {age_sum:.2f}")
print(f"Globalna srednia wieku: {globalna_srednia:.2f}")
