import numpy as np


# Przygotowanie macierzy
np.random.seed(5)
A = np.random.rand(100, 50)
B = np.random.rand(50, 20)

# Mnozenie macierzy za pomoca NumPy
result_numpy = A @ B

# Reczna implementacja mnozenia macierzy
result_manual = np.zeros((A.shape[0], B.shape[1]))

for i in range(A.shape[0]):
    for j in range(B.shape[1]):
        for k in range(A.shape[1]):
            result_manual[i, j] += A[i, k] * B[k, j]

# Porownanie wynikow
results_match = np.allclose(result_numpy, result_manual)

# Prezentacja wynikow
print("MNOZENIE MACIERZY - POROWNANIE")
print("-" * 45)

print("\nKsztalt macierzy A:", A.shape)
print("Ksztalt macierzy B:", B.shape)

print("\nKsztalt wyniku NumPy:", result_numpy.shape)
print("Ksztalt wyniku recznego:", result_manual.shape)

print("\nPierwsze 5x5 elementow wyniku NumPy:")
print(np.round(result_numpy[:5, :5], 4))

print("\nPierwsze 5x5 elementow wyniku recznego:")
print(np.round(result_manual[:5, :5], 4))

print("\nCzy wyniki sa zgodne:", results_match)
