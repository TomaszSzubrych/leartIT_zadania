
# Tworzenie macierzy 10x10 za pomocą zagnieżdżonych list comprehensions
macierz = [
    [i * j for j in range(1, 11)]
    for i in range(1, 11)
]

# Wydruk macierzy w formie tabeli
for wiersz in macierz:
    for wartosc in wiersz:
        print(f"{wartosc:4}", end="")
    print()

