
liczby = [-5, 3, -2, 8, 12, -1, 6, 0, 15, -3]

suma = 0
ile = 0

for temp in liczby:
    if temp > 0:
        suma += temp
        ile += 1

print(f"Suma liczb dodatnich: {suma}")
print(f"Liczba wartości dodatnich: {ile}")
