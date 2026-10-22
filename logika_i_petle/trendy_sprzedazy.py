
sprzedaz = [
    1200, 1350, 1290, 1480, 1520, 1510,
    1680, 1720, 1700, 1890, 1950, 2100
]

liczba_wzrostow = 0
liczba_spadkow = 0
dodatnie_zmiany = []

for i in range(1, len(sprzedaz)):
    poprzednia = sprzedaz[i - 1]
    aktualna = sprzedaz[i]

    zmiana_procentowa = (aktualna - poprzednia) / poprzednia * 100

    if aktualna > poprzednia:
        liczba_wzrostow += 1
        dodatnie_zmiany.append(zmiana_procentowa)

        print(
            f"Miesiąc {i + 1}: wzrost z {poprzednia} do "
            f"{aktualna} (+{zmiana_procentowa:.2f}%)"
        )

    elif aktualna < poprzednia:
        liczba_spadkow += 1

if dodatnie_zmiany:
    sredni_wzrost = sum(dodatnie_zmiany) / len(dodatnie_zmiany)
else:
    sredni_wzrost = 0

print(f"Liczba miesięcy ze wzrostem: {liczba_wzrostow}")
print(f"Liczba miesięcy ze spadkiem: {liczba_spadkow}")
print(f"Średni dodatni wzrost: {sredni_wzrost:.2f}%")
