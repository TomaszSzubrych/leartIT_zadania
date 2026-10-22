
n = 50
liczba = 1
suma = 0

while liczba <= n:
    suma += liczba
    liczba += 1

print(f"Suma liczb od 1 do {n}: {suma}")
print(f"Wynik ze wzoru: {n * (n + 1) // 2}")
