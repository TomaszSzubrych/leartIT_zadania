
liczby_pierwsze = []

for n in range(2, 101):
    czy_pierwsza = True

    for dzielnik in range(2, int(n ** 0.5) + 1):
        if n % dzielnik == 0:
            czy_pierwsza = False
            break

    if czy_pierwsza:
        liczby_pierwsze.append(n)

print(f"Liczby pierwsze: {liczby_pierwsze}")
print(f"Liczba liczb pierwszych: {len(liczby_pierwsze)}")
