
liczby = [-5, 3, -2, 8, 0, -1, 7, 4, -9, 6]

dodatnie = filter(lambda x: x > 0, liczby)

podwojone = list(map(lambda x: x * 2, dodatnie))

print(f"Wynik: {podwojone}")
