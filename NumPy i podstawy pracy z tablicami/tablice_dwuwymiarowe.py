import numpy as np


# Ustalenie ziarna generatora liczb losowych
np.random.seed(0)

# Utworzenie macierzy 5x4 z liczbami od 1 do 50
matrix = np.random.randint(1, 51, size=(5, 4))

# Pobranie drugiego wiersza
second_row = matrix[1]

# Pobranie trzeciej kolumny
third_column = matrix[:, 2]

# Pobranie elementu z pozycji (2, 3)
selected_element = matrix[2, 3]

# Prezentacja wynikow
print("TABLICE DWUWYMIAROWE NUMPY")
print("-" * 40)

print("Utworzona macierz:")
print(matrix)

print("\nKsztalt macierzy:", matrix.shape)
print("Drugi wiersz:", second_row)
print("Trzecia kolumna:", third_column)
print("Element z pozycji (2, 3):", selected_element)
