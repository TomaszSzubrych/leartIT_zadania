
def statystyki(liczby):
    suma = sum(liczby)
    srednia = round(suma / len(liczby), 2)
    minimum = min(liczby)
    maksimum = max(liczby)

    return (suma, srednia, minimum, maksimum)


oceny = [3.5, 4.0, 5.0, 3.0, 4.5, 5.0, 4.0, 3.5]

wynik = statystyki(oceny)

print(f"Suma: {wynik[0]}")
print(f"Średnia: {wynik[1]}")
print(f"Minimum: {wynik[2]}")
print(f"Maksimum: {wynik[3]}")
