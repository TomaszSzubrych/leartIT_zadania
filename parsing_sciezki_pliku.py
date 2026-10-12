
sciezka = "data/processed/train_fold_03_normalized.csv"

elementy = sciezka.split("/")
nazwa_pliku = elementy[2]

czesci = nazwa_pliku.split("_")

folder = elementy[1]
typ_zbioru = czesci[0]
numer_fold = czesci[2]
format_pliku = czesci[3].split(".")[1]

print(f"Folder: {folder}")
print(f"Typ zbioru: {typ_zbioru}")
print(f"Numer fold: {numer_fold}")
print(f"Format pliku: {format_pliku}")
