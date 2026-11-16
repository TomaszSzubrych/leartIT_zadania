import numpy as np


# Utworzenie regularnej siatki 1000x1000 punktow
x = np.linspace(-1, 1, 1000)
y = np.linspace(-1, 1, 1000)

X, Y = np.meshgrid(x, y)

# Sprawdzenie, ktore punkty znajduja sie wewnatrz kola
inside_circle = X ** 2 + Y ** 2 <= 1

# Obliczenie liczby punktow wewnatrz kola i wszystkich punktow
points_inside = np.sum(inside_circle)
total_points = inside_circle.size

# Oszacowanie liczby pi
pi_estimate = 4 * (points_inside / total_points)

# Obliczenie bledu bezwzglednego
absolute_error = abs(pi_estimate - np.pi)

# Prezentacja wynikow
print("OSZACOWANIE PI METODA REGULARNEJ SIATKI")
print("-" * 45)

print("Rozmiar siatki:", X.shape)
print("Liczba wszystkich punktow:", total_points)
print("Liczba punktow wewnatrz kola:", points_inside)

print("\nOszacowana wartosc pi:", pi_estimate)
print("Rzeczywista wartosc pi:", np.pi)
print("Blad bezwzgledny:", absolute_error)

# Tekstowa mapa pierwszych 20x20 punktow
print("\nMAPA PIERWSZYCH 20x20 PUNKTOW")
print("● - punkt w kole | · - punkt poza kolem")

for row in inside_circle[:20, :20]:
    print("".join("●" if point else "·" for point in row))
