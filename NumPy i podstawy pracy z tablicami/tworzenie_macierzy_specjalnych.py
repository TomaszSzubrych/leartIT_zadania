import numpy as np


# Macierz wypelniona zerami
zeros_matrix = np.zeros((3, 3))

# Macierz wypelniona jedynkami
ones_matrix = np.ones((4, 4))

# Macierz identycznosci
identity_matrix = np.eye(5)

# Macierz wypelniona liczba 7
full_matrix = np.full((3, 4), 7)

# Wektor 10 rownoodleglych wartosci od 0 do 1
values = np.linspace(0, 1, 10)

# Prezentacja wynikow
print("TWORZENIE MACIERZY SPECJALNYCH")
print("-" * 40)

print("\nMacierz zerowa 3x3:")
print(zeros_matrix)

print("\nMacierz jedynek 4x4:")
print(ones_matrix)

print("\nMacierz identycznosci 5x5:")
print(identity_matrix)

print("\nMacierz wypelniona liczba 7 (3x4):")
print(full_matrix)

print("\nWektor 10 wartosci od 0 do 1:")
print(values)
