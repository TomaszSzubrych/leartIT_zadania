import numpy as np


# Tablica poczatkowa
arr = np.arange(1, 13)

# Zmiana ksztaltu tablicy
matrix_3x4 = arr.reshape(3, 4)
matrix_2x6 = arr.reshape(2, 6)
matrix_4x3 = arr.reshape(4, 3)

# Splaszczanie tablicy
flattened = matrix_3x4.flatten()
raveled = matrix_3x4.ravel()

# Sprawdzenie roznicy miedzy kopia a widokiem
flatten_copy = matrix_3x4.flatten()
ravel_view = matrix_3x4.ravel()

flatten_copy[0] = 100
ravel_view[1] = 200

# Prezentacja wynikow
print("RESHAPE I FLATTEN")
print("-" * 40)

print("Tablica poczatkowa:", arr)

print("\nKsztalt (3, 4):")
print(matrix_3x4)

print("\nKsztalt (2, 6):")
print(matrix_2x6)

print("\nKsztalt (4, 3):")
print(matrix_4x3)

print("\nWynik flatten():", flattened)
print("Wynik ravel():", raveled)

print("\nPo modyfikacji kopii flatten():")
print(flatten_copy)

print("\nPo modyfikacji widoku ravel():")
print(ravel_view)

print("\nOryginalna macierz po modyfikacji ravel():")
print(matrix_3x4)
