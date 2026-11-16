import numpy as np


# Sygnal wejsciowy i jadro filtra
signal = np.arange(1, 11, dtype=float)
kernel = np.array([0.2, 0.6, 0.2])

# Przygotowanie tablicy wynikowej
result = np.zeros(len(signal) - len(kernel) + 1)

# Reczna konwolucja: petla po pozycjach wyniku
for i in range(len(result)):
    segment = signal[i:i + len(kernel)]
    result[i] = np.sum(segment * kernel)

# Prezentacja wynikow
print("KONWOLUCJA JEDNOWYMIAROWA")
print("-" * 40)

print("\nSygnal wejsciowy:")
print(signal)

print("\nJadro filtra:")
print(kernel)

print("\nWynik konwolucji:")
print(result)

print("\nWYKRES SLUPKOWY WYNIKU")
for i, value in enumerate(result):
    bar = "█" * int(round(value))
    print(f"Pozycja {i}: {bar} ({value:.2f})")
