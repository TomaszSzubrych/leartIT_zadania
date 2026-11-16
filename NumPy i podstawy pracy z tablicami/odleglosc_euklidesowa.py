import numpy as np


# Dwa punkty w przestrzeni 5-wymiarowej
point_a = np.array([1, 2, 3, 4, 5])
point_b = np.array([5, 4, 3, 2, 1])

# Odleglosc euklidesowa miedzy dwoma punktami
distance_ab = np.sqrt(np.sum((point_a - point_b) ** 2))

# Cztery losowe punkty w przestrzeni 5-wymiarowej
np.random.seed(4)
points = np.random.rand(4, 5)

# Roznica wspolrzednych kazdej pary punktow
differences = points[:, np.newaxis, :] - points[np.newaxis, :, :]

# Macierz odleglosci euklidesowych
distance_matrix = np.sqrt(np.sum(differences ** 2, axis=2))

# Prezentacja wynikow
print("ODLEGLOSC EUKLIDESOWA")
print("-" * 40)

print("\nPunkt A:", point_a)
print("Punkt B:", point_b)
print("Odleglosc miedzy punktami A i B:", distance_ab)

print("\nCztery losowe punkty:")
print(np.round(points, 3))

print("\nMacierz odleglosci (4x4):")
print(np.array2string(distance_matrix, precision=3, suppress_small=True))
