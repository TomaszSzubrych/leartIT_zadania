import numpy as np


# Przygotowanie zbioru 50 punktow i punktu zapytania
np.random.seed(10)
data = np.random.rand(50, 2) * 100
query = np.array([50.0, 50.0])

# Obliczenie odleglosci wszystkich punktow od query
differences = data - query
distances = np.sqrt(np.sum(differences ** 2, axis=1))

# Wyznaczenie indeksow pieciu najblizszych punktow
nearest_indices = np.argsort(distances)[:5]

# Prezentacja wynikow
print("K-NEAREST NEIGHBORS")
print("-" * 65)

print("Punkt zapytania:", query)
print("Liczba punktow w zbiorze:", len(data))

print("\nPieciu najblizszych sasiadow:")
print(f"{'Indeks':<10}{'Wspolrzedne':<30}{'Odleglosc':>15}")
print("-" * 55)

for index in nearest_indices:
    coordinates = np.round(data[index], 3)
    distance = distances[index]

    print(f"{index:<10}{str(coordinates):<30}{distance:>15.4f}")
