import numpy as np


# Przygotowanie danych z szumem
np.random.seed(7)
x = np.linspace(0, 10, 100)
y = 2 * x**2 - 3 * x + 5 + np.random.randn(100) * 10

# Utworzenie macierzy cech: [1, x, x^2]
X = np.column_stack((np.ones(len(x)), x, x**2))

# Wyodrebnienie kolumny x^2
x_squared = X[:, 2]

# Obliczenie statystyk kolumny x^2
x_squared_mean = np.mean(x_squared)
x_squared_std = np.std(x_squared)

# Prezentacja wynikow
print("PRZYGOTOWANIE CECH DO REGRESJI WIELOMIANOWEJ")
print("-" * 50)

print("\nKsztalt macierzy X:", X.shape)

print("\nPierwsze 5 wierszy macierzy X:")
print(np.round(X[:5], 4))

print("\nPierwsze 5 wartosci y:")
print(np.round(y[:5], 4))

print("\nStatystyki kolumny x^2:")
print("Srednia:", round(x_squared_mean, 4))
print("Odchylenie standardowe:", round(x_squared_std, 4))
