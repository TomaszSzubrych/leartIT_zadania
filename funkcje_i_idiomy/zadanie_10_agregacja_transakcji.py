
transakcje = [
    {"produkt": "laptop", "wartosc": 2999},
    {"produkt": "mysz", "wartosc": 89},
    {"produkt": "laptop", "wartosc": 2999},
    {"produkt": "klawiatura", "wartosc": 249},
    {"produkt": "mysz", "wartosc": 89},
    {"produkt": "mysz", "wartosc": 89}
]

# Krok 1: Grupowanie i sumowanie za pomocą zwykłej pętli
sumy = {}

for transakcja in transakcje:
    produkt = transakcja["produkt"]
    wartosc = transakcja["wartosc"]

    sumy[produkt] = sumy.get(produkt, 0) + wartosc

# Krok 2: Dictionary comprehension
wynik = {produkt: suma for produkt, suma in sumy.items()}

print("Łączna wartość transakcji:")
print(wynik)
