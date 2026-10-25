
liczby_parzyste = [
    x for x in range(1, 101) if x % 2 == 0
]

print(f"Pierwsze 10 liczb parzystych: {liczby_parzyste[:10]}")
print(f"Liczba wszystkich wartości: {len(liczby_parzyste)}")
